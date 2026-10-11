# CourseHub — Web Database and Information Systems

Project thực hành môn **Cơ sở dữ liệu Web và hệ thống thông tin**, xây dựng hệ thống CourseHub qua ba giai đoạn: xử lý dữ liệu bằng Python, thiết kế và truy vấn cơ sở dữ liệu PostgreSQL, xây dựng REST API bằng FastAPI và kiểm thử bằng Postman.

## 1. Tổng quan project

CourseHub mô phỏng hệ thống quản lý học phần với các nghiệp vụ chính:

- Quản lý sinh viên, học phần, giảng viên và lớp học phần.
- Theo dõi đăng ký học phần của sinh viên.
- Kiểm tra điều kiện đăng ký, phát hiện đăng ký trùng và lớp học phần đã đầy.
- Truy vấn và cập nhật dữ liệu thông qua API.
- Kiểm thử các trường hợp thành công và lỗi.

Project được phát triển theo từng buổi thực hành, từ mô hình dữ liệu trong bộ nhớ đến hệ thống sử dụng cơ sở dữ liệu và backend API.

## 2. Nội dung ba buổi thực hành

### Buổi 1 — Python Fundamentals and Git

Ôn tập các cấu trúc dữ liệu và kỹ thuật lập trình Python cơ bản thông qua bài toán CourseHub.

Nội dung:
- Sử dụng `list` và `dictionary` để mô phỏng dữ liệu.
- Viết hàm tìm kiếm sinh viên và học phần.
- Kiểm tra điều kiện đăng ký học phần.
- Xử lý đăng ký trùng và giới hạn sĩ số.
- Tìm kiếm học phần theo mã hoặc tên.
- Xử lý dữ liệu nhập không hợp lệ bằng `try/except`.
- Thực hành quản lý mã nguồn với Git và GitHub.

File chính: `backend/week01_python_refresh.py`

Chạy chương trình từ thư mục gốc:

```bash
python backend/week01_python_refresh.py
```

### Buổi 2 — PostgreSQL and Relational Database

Xây dựng cơ sở dữ liệu quan hệ cho hệ thống CourseHub.

Nội dung:
- Thiết kế bảng và các mối quan hệ giữa các thực thể.
- Khai báo khóa chính, khóa ngoại và các ràng buộc dữ liệu.
- Khởi tạo dữ liệu mẫu.
- Viết truy vấn SQL để khai thác dữ liệu.
- Thực hành view và kiểm tra các ràng buộc.
- Thực hiện các thao tác dữ liệu trong transaction để quan sát kết quả trước khi rollback.

Các file SQL được lưu trong thư mục `database/`. Ghi chú thực hành nằm tại `docs/week02_notes.md`.

### Buổi 3 — FastAPI, SQLAlchemy Core and Postman

Xây dựng backend REST API kết nối PostgreSQL cho hệ thống CourseHub.

Công nghệ chính:
- **Python** — ngôn ngữ lập trình.
- **FastAPI** — xây dựng REST API.
- **SQLAlchemy Core** — thực thi truy vấn SQL có tham số.
- **PostgreSQL** — hệ quản trị cơ sở dữ liệu.
- **psycopg** — driver kết nối PostgreSQL.
- **Pydantic** — kiểm tra dữ liệu đầu vào và đầu ra.
- **Postman** — kiểm thử API.

Các chức năng API bao gồm:
- Kiểm tra trạng thái ứng dụng và kết nối cơ sở dữ liệu.
- Liệt kê, tìm kiếm học phần và xem thông tin học phần.
- Liệt kê giảng viên và lớp học phần.
- Xem danh sách đăng ký của sinh viên.
- Tạo đăng ký học phần và kiểm tra các điều kiện nghiệp vụ.
- Hủy đăng ký học phần.
- Cập nhật sức chứa lớp học phần.
- Xử lý các trường hợp dữ liệu không hợp lệ, bản ghi không tồn tại, đăng ký trùng và lớp đã đầy.

Các file chính:

- `backend/app/main.py` — khai báo các endpoint.
- `backend/app/database.py` — cấu hình kết nối PostgreSQL.
- `backend/app/schemas.py` — định nghĩa schema dữ liệu.
- `backend/requirements.txt` — danh sách thư viện cần cài đặt.
- `backend/.env.example` — mẫu cấu hình môi trường.
- `docs/week03_notes.md` — hướng dẫn thực hành Buổi 3.
- `postman/` — collection và environment phục vụ kiểm thử API.

## 3. Cấu trúc repository

```text
coursehub-demo/
├── .gitignore
├── README.md
├── backend/
│   ├── __init__.py
│   ├── week01_python_refresh.py
│   ├── .env.example
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── database.py
│       ├── schemas.py
│       └── main.py
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   ├── 03_queries.sql
│   ├── 04_views.sql
│   ├── 05_constraint_checks.sql
│   ├── 06_view_demo.sql
│   └── 07_ai_query.sql
├── docs/
│   ├── week02_notes.md
│   └── week03_notes.md
└── postman/
    ├── collections/
    ├── environments/
    └── globals/
```

File `backend/.env` được tạo riêng trên máy chạy ứng dụng và không đưa lên repository. Các thư mục môi trường ảo như `.venv/`, cache Python và file `.pyc` cũng không được commit.

## 4. Yêu cầu môi trường

Trước khi chạy Buổi 3, cần chuẩn bị:

- Python tương thích với các thư viện trong `backend/requirements.txt`.
- PostgreSQL đã cài đặt và đang chạy.
- Cơ sở dữ liệu CourseHub đã được khởi tạo theo hướng dẫn Buổi 2.
- Thông tin kết nối PostgreSQL hợp lệ.
- Postman nếu muốn chạy bộ kiểm thử API.

## 5. Cài đặt và cấu hình Buổi 3

Các lệnh dưới đây được chạy từ thư mục gốc `coursehub-demo`.

### Bước 1 — Tạo môi trường Python

Nếu chưa có môi trường ảo:

```bash
python -m venv .venv
```

Kích hoạt trên Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Kích hoạt trên Git Bash:

```bash
source .venv/Scripts/activate
```

### Bước 2 — Cài đặt thư viện

```bash
python -m pip install -r backend/requirements.txt
```

### Bước 3 — Cấu hình biến môi trường

Sao chép `backend/.env.example` thành `backend/.env`, sau đó điền thông tin PostgreSQL của máy đang sử dụng.

Ví dụ định dạng:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=coursehub
DB_USER=coursehub_user
DB_PASSWORD=THAY_BANG_MAT_KHAU_CUA_BAN
```

Thay giá trị mật khẩu mẫu bằng mật khẩu thực tế. Không commit file `backend/.env` lên GitHub.

### Bước 4 — Khởi động API

```bash
python -m uvicorn backend.app.main:app --reload
```

Sau khi ứng dụng khởi động thành công, có thể truy cập:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Swagger UI cho phép xem các endpoint và gửi request trực tiếp từ trình duyệt.

## 6. Kiểm thử API bằng Postman

Import collection CourseHub và environment tương ứng từ thư mục `postman/` theo định dạng được lưu trong repository.

Thiết lập biến `base_url` trong environment:

```text
http://127.0.0.1:8000
```

Đảm bảo backend đang chạy và cơ sở dữ liệu đã có dữ liệu cần thiết trước khi thực hiện kiểm thử.

Quy trình kiểm thử gợi ý:

1. Gọi endpoint kiểm tra trạng thái ứng dụng.
2. Lấy danh sách học phần và lớp học phần.
3. Tra cứu thông tin học phần hoặc đăng ký của sinh viên.
4. Tạo đăng ký học phần hợp lệ.
5. Thử đăng ký trùng hoặc đăng ký vào lớp đã đầy.
6. Thử các request có dữ liệu thiếu hoặc mã không tồn tại.
7. Hủy đăng ký và kiểm tra lại dữ liệu.

Kết quả cụ thể phụ thuộc vào dữ liệu đang có trong PostgreSQL. Khi kiểm thử các request làm thay đổi dữ liệu, cần kiểm tra trạng thái cơ sở dữ liệu để tránh ảnh hưởng đến các lần chạy tiếp theo.

## 7. Git và GitHub

Repository:

https://github.com/Hoanghung1008/coursehub-demo

Các nhánh thực hành:
- `week_1` — Buổi 1.
- `week_2` — Buổi 2.
- `week_3` — Buổi 3.

Mỗi nhánh được sử dụng để lưu và nộp nội dung tương ứng với buổi thực hành. README trên nhánh `week_3` mô tả tổng quan cả project và hướng dẫn chạy phần backend của Buổi 3.

Sau khi thay đổi mã nguồn, có thể kiểm tra và commit bằng:

```bash
git status
git diff
git add README.md
git commit -m "Update README for CourseHub week 3"
git push
```

Nếu đang làm trên nhánh `week_3`, lệnh `git push` sẽ đẩy commit lên nhánh tương ứng khi upstream đã được cấu hình.

## 8. Lưu ý

- Khởi tạo PostgreSQL và cấu hình đúng thông tin kết nối trước khi chạy API.
- Không đưa mật khẩu hoặc thông tin bí mật vào mã nguồn hay commit Git.
- Không giả định mọi request Postman đều thành công: kết quả phụ thuộc vào dữ liệu và trạng thái hiện tại của cơ sở dữ liệu.
- Nên đọc `docs/week02_notes.md` và `docs/week03_notes.md` để xem hướng dẫn chi tiết của từng buổi.
- Mã nguồn và các thao tác kiểm thử cần được kiểm tra trước khi sử dụng hoặc nộp bài.
