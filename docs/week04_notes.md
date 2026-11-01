# CourseHub - Buoi 4

- **Migration 001:** Tạo bảng `enrollment_events` để lưu lịch sử đăng ký và hủy đăng ký. Bảng `schema_migrations` lưu phiên bản migration đã áp dụng. Các loại sự kiện gồm `CREATED` và `CANCELLED`. Có file rollback tương ứng.

- **Demo class:** `RACE-01`, `capacity = 1`. Lớp được sử dụng để tái hiện race condition và kiểm thử cơ chế khóa bản ghi.

- **Race condition:** Khi hai transaction đồng thời kiểm tra số chỗ trống rồi đăng ký mà không sử dụng khóa, cả hai request đều có thể thành công. Kết quả thực nghiệm là `enrolled = 2`, vượt quá sức chứa 1.

- **POST /enrollments:** Sử dụng `SELECT ... FOR UPDATE` để khóa dòng `class_sections` trước khi kiểm tra sức chứa và INSERT. Việc tạo đăng ký và ghi audit event `CREATED` được thực hiện trong cùng transaction.

- **DELETE /enrollments/{student_id}/{class_section_id}:** Khóa dòng lớp học trước khi hủy đăng ký. Việc xóa đăng ký và ghi audit event `CANCELLED` được thực hiện trong cùng transaction.

- **Concurrency test:** Sử dụng `ThreadPoolExecutor` và `threading.Barrier` để gửi hai request đồng thời. Kết quả: một request HTTP `201`, một request HTTP `409`. Trạng thái cuối của `RACE-01`: `enrolled_count = 1`, `remaining_slots = 0`.

- **Performance data:** Sinh 100.000 bản ghi bằng `generate_series(1, 100000)`, gắn `dataset = 'performance'`. Kết quả kiểm tra tại thời điểm thực nghiệm: `demo = 3`, `performance = 100000`.

- **Index:** Tạo composite index `idx_enrollment_events_dataset_student_time` trên các cột `(dataset, student_id, occurred_at DESC)`.

- **Query performance:** Sử dụng `EXPLAIN (ANALYZE, BUFFERS)` để đo cùng một truy vấn trước và sau khi tạo index.

  | Tiêu chí | Trước index | Sau index |
  |---|---:|---:|
  | Scan type | Seq Scan | Index Scan |
  | Execution Time | 6.257 ms | 0.299 ms |
  | Planning Time | 1.496 ms | 0.360 ms |
  | Sort riêng | Có | Không |
  | Số dòng trả về | 50 | 50 |

  Trước index, PostgreSQL loại bỏ 99.183 dòng không thỏa mãn điều kiện lọc. Sau index, PostgreSQL sử dụng Index Scan và không cần bước Sort riêng. Thời gian thực thi giảm khoảng 20.9 lần trong lần đo này.

- **SQL Injection:** Kiểm thử endpoint `GET /courses?q=...` bằng payload `%25%27%20OR%20%271%27%3D%271%27--`. Kết quả HTTP `200 OK`, response `[]`. API sử dụng bind parameters (`:keyword`) để tách dữ liệu đầu vào khỏi cấu trúc câu SQL.

**Kết luận:** Buổi thực hành đã tái hiện được race condition, áp dụng row-level locking để kiểm soát đăng ký đồng thời, ghi nhận audit event trong transaction và đánh giá hiệu năng truy vấn trước/sau khi tạo composite index.
