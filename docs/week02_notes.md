# CourseHub - Buổi 2

## 1. Tổng quan

Buổi thực hành xây dựng cơ sở dữ liệu CourseHub trên PostgreSQL, chuyển dữ liệu từ ví dụ Python của Buổi 1 sang mô hình dữ liệu quan hệ gồm sáu bảng có liên kết với nhau.

### Thông tin môi trường

- **Database:** `coursehub`
- **Database engine:** PostgreSQL
- **Tài khoản thực hành:** `coursehub_user`

Dữ liệu trong bài là dữ liệu minh họa phục vụ thực hành, không phải dữ liệu quản lý đào tạo chính thức.

---

## 2. Cấu trúc cơ sở dữ liệu

Hệ thống gồm sáu bảng:

| Bảng | Mục đích |
|---|---|
| `students` | Lưu thông tin sinh viên |
| `courses` | Lưu thông tin học phần |
| `semesters` | Lưu thông tin học kỳ |
| `lecturers` | Lưu thông tin giảng viên |
| `class_sections` | Lưu thông tin lớp học phần |
| `enrollments` | Lưu thông tin đăng ký lớp học phần |

### Quan hệ giữa các bảng

```text
class_sections.course_code
    → courses.code

class_sections.semester_code
    → semesters.code

class_sections.lecturer_id
    → lecturers.id

enrollments.student_id
    → students.id

enrollments.class_section_id
    → class_sections.id
```

Các ràng buộc được sử dụng:

- `PRIMARY KEY`
- `FOREIGN KEY`
- `UNIQUE`
- `NOT NULL`
- `CHECK`

Khóa chính của bảng `enrollments` là khóa ghép:

```text
(student_id, class_section_id)
```

Ràng buộc này ngăn một sinh viên đăng ký trùng cùng một lớp học phần.

---

## 3. Thứ tự khởi tạo

Các tệp SQL được sử dụng theo thứ tự:

```text
01_schema.sql
↓
02_seed.sql
↓
04_views.sql
```

Trong đó:

- `01_schema.sql`: Tạo sáu bảng và các ràng buộc.
- `02_seed.sql`: Nhập bộ dữ liệu mẫu.
- `03_queries.sql`: Thực hiện các truy vấn tra cứu và thống kê.
- `04_views.sql`: Tạo và khai thác view `v_section_summary`.
- `05_constraint_checks.sql`: Kiểm tra các ràng buộc bằng dữ liệu sai có chủ ý.
- `06_view_demo.sql`: Minh họa giao dịch `BEGIN → INSERT → SELECT → ROLLBACK → SELECT`.
- `07_ai_query.sql`: Đối chiếu truy vấn SQL đếm đúng và đếm sai.

---

## 4. Bộ dữ liệu chuẩn

Sau khi khởi tạo thành công, cơ sở dữ liệu có:

| Đối tượng | Số lượng |
|---|---:|
| Sinh viên | 4 |
| Học phần | 3 |
| Học kỳ | 1 |
| Giảng viên | 2 |
| Lớp học phần | 4 |
| Lượt đăng ký | 5 |

### Trạng thái các lớp học phần

| Lớp | Học phần | Sức chứa | Số đăng ký | Số chỗ còn lại |
|---|---|---:|---:|---:|
| `DM-01` | `INT2205` | 2 | 2 | 0 |
| `PY-01` | `INT2206` | 2 | 1 | 1 |
| `WEB-01` | `INT2204` | 3 | 2 | 1 |
| `WEB-02` | `INT2204` | 2 | 0 | 2 |

Bộ dữ liệu chuẩn này được sử dụng xuyên suốt các truy vấn và ví dụ trong Buổi 2.

---

## 5. Các truy vấn SQL

### 5.1. Tra cứu học phần

`03_queries.sql` thực hiện các truy vấn:

- Hiển thị danh sách học phần.
- Tìm học phần theo một phần mã hoặc tên.
- Xem các lớp mà một sinh viên đã đăng ký.
- Đếm số đăng ký và số chỗ còn lại của từng lớp.
- Tìm sinh viên chưa đăng ký lớp nào.
- Sử dụng CTE để tách các bước xử lý.
- Xếp hạng học phần theo số lượt đăng ký bằng hàm cửa sổ.

### 5.2. Kết quả chính

Học phần có số lượt đăng ký cao nhất:

| Học phần | Số lượt đăng ký | Hạng |
|---|---:|---:|
| `INT2204` | 2 | 1 |
| `INT2205` | 2 | 1 |
| `INT2206` | 1 | 2 |

`INT2204` và `INT2205` có cùng số lượt đăng ký nên cùng hạng `1`.

### 5.3. Lớp còn chỗ

Các lớp còn chỗ:

| Lớp | Sức chứa | Đã đăng ký | Còn lại |
|---|---:|---:|---:|
| `PY-01` | 2 | 1 | 1 |
| `WEB-01` | 3 | 2 | 1 |
| `WEB-02` | 2 | 0 | 2 |

Trong truy vấn sử dụng `LEFT JOIN`, cần dùng:

```sql
COUNT(e.student_id)
```

thay vì:

```sql
COUNT(*)
```

để lớp chưa có đăng ký được tính là `0`.

---

## 6. Kiểm tra các ràng buộc

File `05_constraint_checks.sql` chứa các thao tác cố ý tạo dữ liệu không hợp lệ để kiểm tra ràng buộc của database.

Các trường hợp đã kiểm tra:

1. Đăng ký trùng một lớp.
2. Đăng ký với sinh viên không tồn tại.
3. Đặt sức chứa lớp bằng `0`.
4. Gán `NULL` cho số tín chỉ.
5. Sử dụng email đã tồn tại.
6. Nhập họ tên chỉ gồm khoảng trắng.

Các lệnh trên đều bị PostgreSQL từ chối đúng theo thiết kế.

### Kiểm tra sau khi thử lỗi

Tổng số lượt đăng ký vẫn giữ nguyên:

```text
5
```

Q4 cũng được chạy lại và cho kết quả ban đầu:

```text
DM-01   INT2205   2   2   0
PY-01   INT2206   2   1   1
WEB-01  INT2204   3   2   1
WEB-02  INT2204   2   0   2
```

---

## 7. View tổng hợp

Database sử dụng view:

```text
v_section_summary
```

View cung cấp các thông tin:

- `class_id`
- `course_code`
- `capacity`
- `enrolled`
- `remaining`

View được xây dựng từ `class_sections` và `enrollments`.

Số lượng đăng ký được tính trực tiếp từ bảng `enrollments`, vì vậy không cần lưu riêng một cột `enrolled` trong `class_sections`.

### Khai thác View

Các lớp còn chỗ thông qua view:

```text
PY-01   1
WEB-01  1
WEB-02  2
```

---

## 8. Kiểm tra giao dịch

File `06_view_demo.sql` minh họa quy trình:

```text
BEGIN
↓
INSERT
↓
SELECT
↓
ROLLBACK
↓
SELECT
```

Hoàng Nam (`22000004`) được sử dụng để thử đăng ký lớp `WEB-01`.

### Trạng thái trong giao dịch

Sau khi đăng ký thử:

```text
class_id   = WEB-01
capacity   = 3
enrolled   = 3
remaining  = 0
```

Sau khi thực hiện:

```sql
ROLLBACK;
```

trạng thái trở về:

```text
class_id   = WEB-01
capacity   = 3
enrolled   = 2
remaining  = 1
```

Tổng số lượt đăng ký của database vẫn là `5`.

---

## 9. Kiểm tra truy vấn do AI đề xuất

File `07_ai_query.sql` minh họa trường hợp một câu SQL có thể chạy thành công nhưng vẫn cho kết quả sai về nghiệp vụ.

### Truy vấn sai

```sql
SELECT cs.id, COUNT(*) AS enrolled
FROM class_sections AS cs
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
WHERE cs.id = 'WEB-02'
GROUP BY cs.id;
```

Kết quả:

```text
WEB-02 | 1
```

Kết quả này sai vì `WEB-02` thực tế chưa có sinh viên đăng ký.

### Truy vấn đúng

```sql
SELECT cs.id, COUNT(e.student_id) AS enrolled
FROM class_sections AS cs
LEFT JOIN enrollments AS e ON e.class_section_id = cs.id
WHERE cs.id = 'WEB-02'
GROUP BY cs.id;
```

Kết quả:

```text
WEB-02 | 0
```

Nguyên nhân là `LEFT JOIN` vẫn giữ lại dòng của `WEB-02` khi chưa có dữ liệu khớp. `COUNT(*)` đếm cả dòng đó, trong khi `COUNT(e.student_id)` chỉ đếm các `student_id` có giá trị.

---

## 10. Cấu trúc tệp

```text
coursehub-demo/
├── backend/
│   └── week01_python_refresh.py
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   ├── 03_queries.sql
│   ├── 04_views.sql
│   ├── 05_constraint_checks.sql
│   ├── 06_view_demo.sql
│   └── 07_ai_query.sql
├── docs/
│   └── week02_notes.md
├── .gitignore
└── README.md
```

### Lưu ý khi sử dụng

Các tệp `.sql` chứa cấu trúc hoặc câu lệnh SQL, không phải bản sao của dữ liệu đang chạy trong PostgreSQL.

Khi clone repository sang máy khác, database `coursehub` không tự động được tạo. Cần kết nối PostgreSQL và chạy lại các tệp khởi tạo theo đúng thứ tự.

Không lưu mật khẩu PostgreSQL hoặc thông tin xác thực vào repository.

---

## 11. Trạng thái hoàn thành

Buổi 2 đã hoàn thành các nội dung:

- Tạo database `coursehub`.
- Tạo tài khoản `coursehub_user`.
- Tạo sáu bảng quan hệ.
- Thiết lập các ràng buộc dữ liệu.
- Nhập bộ dữ liệu mẫu.
- Thực hiện các truy vấn `SELECT`, `JOIN`, `GROUP BY`, `NOT EXISTS`.
- Sử dụng CTE và hàm cửa sổ.
- Tạo và khai thác view.
- Kiểm tra các ràng buộc bằng dữ liệu sai.
- Minh họa transaction với `ROLLBACK`.
- Kiểm tra và sửa truy vấn SQL do AI đề xuất.
