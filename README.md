# CourseHub - Buổi 1

Project thực hành môn **Cơ sở dữ liệu Web và hệ thống thông tin**.

Buổi 1 tập trung vào việc làm quen với mô hình hệ thống thông tin Web, ôn tập các cấu trúc Python cơ bản, mô phỏng dữ liệu CourseHub bằng Python và thực hành quản lý mã nguồn bằng Git/GitHub.

> **Phạm vi:** Buổi 1 chưa sử dụng cơ sở dữ liệu thật. Dữ liệu được mô phỏng bằng `list` và `dictionary` trong Python.

---

## 1. Mục tiêu

Project thực hiện các nội dung chính của Buổi 1:

- Ôn tập `list` và `dictionary`.
- Sử dụng điều kiện và vòng lặp để xử lý dữ liệu.
- Tách xử lý thành các hàm.
- Sử dụng `try/except` để xử lý dữ liệu nhập sai.
- Tìm kiếm sinh viên và học phần.
- Tìm kiếm học phần theo mã hoặc tên.
- Mô phỏng quy tắc đăng ký học phần.
- Thực hiện kiểm thử nhiều tình huống.
- Thực hành quy trình `git status` → `git diff` → `git add` → `git commit` → `git push`.

---

## 2. Bài toán CourseHub

CourseHub là hệ thống mô phỏng việc quản lý:

- Sinh viên.
- Học phần.
- Đăng ký học phần.

Một số quy tắc nghiệp vụ cơ bản được mô phỏng:

1. Sinh viên phải tồn tại.
2. Học phần phải tồn tại.
3. Sinh viên không được đăng ký trùng cùng một học phần.
4. Lớp học phần phải còn chỗ.
5. Khi đăng ký thành công, hệ thống phải tạo bản ghi đăng ký và cập nhật sĩ số.

Ở các buổi sau, các dữ liệu và quy tắc này sẽ được kết hợp với backend/API và cơ sở dữ liệu.

---

## 3. Cấu trúc project

```text
coursehub-demo/
├── .gitignore
├── README.md
└── backend/
    └── week01_python_refresh.py
```

### Các file

**`.gitignore`**

Chứa các tệp/thư mục không cần đưa vào Git repository, ví dụ:

- `__pycache__/`
- `*.pyc`
- `.venv/`
- `.env`

**`README.md`**

Mô tả project, phạm vi thực hành, chức năng, kiểm thử và cách chạy.

**`backend/week01_python_refresh.py`**

Chứa toàn bộ phần thực hành Python của Buổi 1.

---

## 4. Dữ liệu mô phỏng

### Sinh viên

Project hiện có hai sinh viên:

```text
22000001 - Nguyen Minh Anh - KHDL
22000002 - Tran Duc Long - KHDL
```

### Học phần

```text
INT2204 - Co so du lieu Web va he thong thong tin
capacity = 3
enrolled = 2

INT2205 - Khai pha du lieu
capacity = 2
enrolled = 2
```

### Đăng ký ban đầu

```text
22000001 -> INT2204
```

Dữ liệu trên chỉ tồn tại trong bộ nhớ khi chương trình đang chạy.

---

## 5. Các hàm chính

### `find_student(student_id)`

Tìm sinh viên theo mã sinh viên.

Nếu tìm thấy, hàm trả về dictionary tương ứng.

Nếu không tìm thấy, hàm trả về `None`.

---

### `find_course(course_code)`

Tìm học phần theo mã học phần.

Nếu tìm thấy, hàm trả về dictionary tương ứng.

Nếu không tìm thấy, hàm trả về `None`.

---

### `is_enrolled(student_id, course_code)`

Kiểm tra sinh viên đã đăng ký học phần hay chưa.

Hàm trả về:

```text
True
```

nếu đã tồn tại bản ghi đăng ký và:

```text
False
```

nếu chưa đăng ký.

---

### `can_enroll(student_id, course_code)`

Kiểm tra các điều kiện để sinh viên có thể đăng ký học phần:

1. Sinh viên tồn tại.
2. Học phần tồn tại.
3. Sinh viên chưa đăng ký học phần.
4. Lớp còn chỗ.

Hàm trả về một tuple gồm:

```text
(True, "Co the dang ky")
```

hoặc:

```text
(False, "Ly do")
```

---

### `enroll_student(student_id, course_code)`

Thực hiện đăng ký học phần.

Nếu các điều kiện không hợp lệ, hàm trả về lỗi tương ứng.

Nếu đăng ký thành công:

- Thêm bản ghi mới vào `enrollments`.
- Tăng `enrolled` của học phần lên 1.

---

### `search_courses(keyword)`

Tìm kiếm học phần theo:

- Mã học phần.
- Tên học phần.

Đặc điểm:

- Không phân biệt chữ hoa/chữ thường.
- Loại bỏ khoảng trắng thừa ở đầu và cuối từ khóa.
- Trả về danh sách các học phần phù hợp.

---

### `get_remaining_slots(course)`

Tính số chỗ còn lại:

```text
remaining = capacity - enrolled
```

---

## 6. Xử lý input

Chương trình có phần nhập số lượng học phần muốn hiển thị:

```text
Nhap so luong hoc phan muon hien thi:
```

Dữ liệu nhập được chuyển sang số nguyên bằng `int()`.

Trường hợp người dùng nhập dữ liệu không hợp lệ, `try/except` được sử dụng để xử lý `ValueError` thay vì làm chương trình dừng đột ngột.

---

## 7. Kiểm thử

Project thực hiện tối thiểu 05 tình huống theo yêu cầu bài thực hành.

### Test 1 — Đăng ký thành công

Sinh viên:

```text
22000002
```

đăng ký:

```text
INT2204
```

Kết quả:

```text
(True, 'Dang ky thanh cong')
```

---

### Test 2 — Đăng ký trùng

Sinh viên `22000002` tiếp tục đăng ký `INT2204`.

Kết quả:

```text
(False, 'Sinh vien da dang ky hoc phan nay')
```

---

### Test 3 — Lớp đã đầy

Đăng ký vào học phần:

```text
INT2205
```

với:

```text
capacity = 2
enrolled = 2
```

Kết quả:

```text
(False, 'Lop da du so luong')
```

---

### Test 4 — Học phần không tồn tại

Sử dụng mã học phần:

```text
INT9999
```

Kết quả:

```text
(False, 'Hoc phan khong ton tai')
```

---

### Test 5 — Sinh viên không tồn tại

Sử dụng mã sinh viên:

```text
99999999
```

Kết quả:

```text
(False, 'Sinh vien khong ton tai')
```

---

## 8. Cách chạy chương trình

Từ thư mục gốc `coursehub-demo`, chạy:

```bash
python backend/week01_python_refresh.py
```

Khi chương trình yêu cầu:

```text
Nhap so luong hoc phan muon hien thi:
```

có thể nhập:

```text
2
```

Sau đó kiểm tra toàn bộ kết quả hiển thị, đặc biệt là 05 test ở cuối chương trình.

---

## 9. Git và GitHub

### Repository

```text
https://github.com/Hoanghung1008/coursehub-demo
```

### Branch dùng để nộp bài

```text
week_1
```

### Link branch nộp bài

```text
https://github.com/Hoanghung1008/coursehub-demo/tree/week_1
```

Repository cần ở chế độ **Public** để giảng viên có thể truy cập và chấm bài.

---

## 10. Quy trình Git sau khi chỉnh sửa

Sau khi sửa mã nguồn:

```bash
git status
git diff
git add backend/week01_python_refresh.py
git commit -m "Describe the change"
git push
```

Kiểm tra lại:

```bash
git status
```

Kết quả mong muốn:

```text
nothing to commit, working tree clean
```

Và branch hiện tại phải là:

```text
week_1
```

---

## 11. Phạm vi của Buổi 1

Project này cố ý chỉ sử dụng Python và dữ liệu mô phỏng trong bộ nhớ.

Chưa sử dụng:

- FastAPI.
- PostgreSQL.
- ORM.
- API thực tế.
- Frontend.

Các thành phần trên thuộc các phần thực hành tiếp theo của học phần.

---

## 12. Lưu ý

Mã nguồn cần được đọc, chạy thử và kiểm tra trước khi commit.

Việc sử dụng công cụ AI chỉ nhằm hỗ trợ giải thích, phân tích và phát hiện lỗi. Mã nguồn cuối cùng phải được kiểm tra và hiểu trước khi đưa lên repository.