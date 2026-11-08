# CourseHub - Buoi 5: React Frontend and FastAPI Integration

## 1. Muc tieu

- Xay dung giao dien Frontend bang React va Vite.
- Ket noi Frontend voi Backend FastAPI thong qua HTTP API.
- Cau hinh CORS cho phep trinh duyet truy cap Backend.
- Hien thi danh sach hoc phan, lop hoc phan va lop sinh vien da dang ky.
- Ho tro tim kiem va loc lop con cho.
- Ho tro dang ky va huy dang ky lop hoc phan.
- Xu ly cac trang thai loading, empty, success va error.

## 2. Cau truc Frontend

Cac tep duoc tao va su dung trong Buoi 5:

```text
frontend/
├── .env.example
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── tests/
│   └── api.test.mjs
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api.js
    ├── styles.css
    └── components/
        ├── Notice.jsx
        ├── SectionTable.jsx
        └── EnrollmentList.jsx
```

Vai tro cac tep:

- `frontend/src/main.jsx`: diem khoi chay ung dung React.
- `frontend/src/App.jsx`: dieu phoi du lieu, trang thai va thao tac giao dien.
- `frontend/src/api.js`: cac ham goi API va xu ly loi HTTP.
- `frontend/src/styles.css`: giao dien va bo cuc responsive.
- `frontend/src/components/Notice.jsx`: hien thi thong bao.
- `frontend/src/components/SectionTable.jsx`: hien thi danh sach lop hoc phan.
- `frontend/src/components/EnrollmentList.jsx`: hien thi danh sach lop da dang ky.
- `frontend/tests/api.test.mjs`: kiem thu cac ham goi API.
- `frontend/.env.example`: mau cau hinh URL Backend.

## 3. Cau hinh Backend va CORS

Backend tiep tuc su dung ma nguon va nghiep vu cua Buoi 4.

Bo sung CORS trong `backend/app/main.py` de cho phep Frontend truy cap Backend tu cac dia chi local:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

Cac HTTP methods duoc cho phep:

- GET
- POST
- DELETE
- PATCH
- OPTIONS

Khong thay doi logic transaction, row lock va ghi nhat ky `enrollment_events` cua Buoi 4.

## 4. Cau hinh Frontend

File `frontend/.env.example`:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

File `.env.local` duoc tao rieng tren may de chay Frontend, khong dua len GitHub.

Cac thu muc va tep khong commit:

- `frontend/.env.local`
- `frontend/node_modules/`
- `frontend/dist/`

## 5. Cach chay ung dung

Su dung repository va database CourseHub hien tai tu Buoi 4. Khong khoi tao lai database.

### 5.1. Chay Backend

Tai thu muc goc repository, kich hoat moi truong Python va chay:

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend API:

```text
http://127.0.0.1:8000/
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### 5.2. Chay Frontend

Mo Terminal khac:

```bash
cd frontend
npm install
npm run dev
```

Truy cap giao dien:

```text
http://127.0.0.1:5173/
```

Can giu ca Backend va Frontend dang chay trong khi kiem tra ung dung.

## 6. Cac chuc nang da xay dung

### 6.1. Chon sinh vien

- Nhap ma sinh vien.
- Kiem tra dinh dang ma sinh vien.
- Tai lai danh sach dang ky theo sinh vien duoc chon.

### 6.2. Danh sach lop hoc phan

- Hien thi ma lop, hoc phan va suc chua.
- Hien thi so luong sinh vien da dang ky.
- Hien thi so cho con lai.
- Tim kiem lop hoc phan.
- Loc cac lop con cho.
- Vo hieu hoa thao tac dang ky khi lop da day hoac sinh vien da dang ky.

### 6.3. Danh sach lop da dang ky

- Hien thi cac lop sinh vien dang tham gia.
- Cho phep huy dang ky.
- Hien thi trang thai khi danh sach rong.

### 6.4. Xu ly ket qua API

Frontend xu ly cac truong hop:

- HTTP 201: dang ky thanh cong.
- HTTP 204: huy dang ky thanh cong, khong doc JSON response.
- HTTP 404: khong tim thay sinh vien hoac lop hoc phan.
- HTTP 409: dang ky trung hoac lop hoc phan da day.
- Loi ket noi: thong bao khong the ket noi Backend.

Sau khi dang ky hoac huy dang ky, Frontend tai lai du lieu tu Backend thay vi tu thay doi so luong cho trong giao dien.

## 7. Kiem thu

### 7.1. Kiem thu tu dong

Chay tai thu muc `frontend`:

```bash
npm test
npm run build
```

Ket qua da thuc hien:

| Hang muc | Ket qua |
|---|---|
| `npm test` | PASS |
| So luong test | 8/8 |
| Test that bai | 0 |
| `npm run build` | PASS |
| Vite production build | Thanh cong |

Cac test trong `tests/api.test.mjs` su dung HTTP gia lap de kiem tra ham goi API. Cac test nay khong thay the kiem thu truc tiep voi PostgreSQL hoac kiem thu concurrency.

### 7.2. Kiem tra giao dien

Da kiem tra:

- Frontend khoi dong bang Vite.
- Trinh duyet mo duoc giao dien CourseHub.
- Hien thi danh sach lop hoc phan tu Backend.
- Hien thi danh sach lop da dang ky cua sinh vien `22000004`.
- Hien thi suc chua, so luong da dang ky va so cho con lai.

### 7.3. Kiem tra dang ky va huy dang ky

Trang thai: CHO KIEM TRA LAI tren phien ban giao dien hien tai.

Can doi chieu:

- Request POST va HTTP status tra ve.
- Request DELETE va HTTP status tra ve.
- Danh sach dang ky sau moi thao tac.
- So cho con lai sau khi tai lai du lieu.
- Du lieu PostgreSQL va nhat ky `enrollment_events`.

Khong ghi nhan ket qua PASS khi chua kiem tra truc tiep tren phien ban hien tai.

## 8. Kiem tra PostgreSQL

Su dung tep:

```text
database/13_week05_verify.sql
```

Cac truy van trong tep chi doc du lieu, dung de doi chieu:

1. Suc chua va so luong dang ky cua WEB-01, RACE-01.
2. Danh sach lop hoc phan cua sinh vien `22000004`.
3. Nhat ky tao va huy dang ky WEB-01 trong dataset demo.

Chay tung truy van trong Query Tool cua pgAdmin.

Khong chay lai schema, seed hoac cac script reset tren database CourseHub hien tai.

## 9. Wireframe giao dien

Theo yeu cau Buoi 5, wireframe can the hien:

- Khu vuc chon ma sinh vien.
- Danh sach lop hoc phan.
- Danh sach lop sinh vien da dang ky.
- Trang thai dang ky thanh cong.
- Trang thai lop hoc phan da day.

Link Figma hoac tep wireframe xuat ra: CHUA BO SUNG.

## 10. Luu y

- Tiep tuc su dung database CourseHub da co tu Buoi 4.
- Khong chay lai schema, seed hoac migration da thuc hien tren database hien tai.
- Khong chay cac script thu loi, reset hoac rollback neu khong co yeu cau rieng.
- Giu nguyen transaction, row lock va logic ghi `enrollment_events` cua Backend Buoi 4.
- Khong commit `.env`, `.env.local`, `node_modules` hoac `dist`.
- Bao cao ket qua kiem thu phai phan biet ro cac hang muc da kiem tra va cac hang muc con cho kiem tra lai.
c