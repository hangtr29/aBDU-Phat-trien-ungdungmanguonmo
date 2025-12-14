# Hướng dẫn chạy dự án nhanh

## Bước 1: Chạy lại migration (đã sửa lỗi encoding)

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d elearning -f database/add_user_balance.sql
```

Mật khẩu: `mat_khau_moi`

## Bước 2: Tạo file .env

Tạo file `fastapi_app/.env` với nội dung:

```env
DATABASE_URL=postgresql+psycopg://postgres:mat_khau_moi@localhost:5432/elearning
JWT_SECRET=your-secret-key-here-change-in-production-123456
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Lưu ý:** Thay `mat_khau_moi` bằng mật khẩu PostgreSQL của bạn.

## Bước 3: Chạy dự án

### Cách 1: Chạy tự động (Khuyến nghị)

```powershell
.\start-dev.ps1
```

Script sẽ tự động:
- Activate virtual environment
- Cài đặt frontend dependencies (nếu chưa có)
- Chạy Backend (port 8001)
- Chạy Frontend (port 3000)

### Cách 2: Chạy thủ công

**Terminal 1 - Backend:**
```powershell
.\venv\Scripts\Activate.ps1
uvicorn fastapi_app.main:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm install  # Chỉ cần chạy lần đầu
npm run dev
```

## Bước 4: Truy cập

- **Frontend:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8001
- **API Docs:** http://127.0.0.1:8001/docs

## Troubleshooting

### Lỗi: "Module not found"
```powershell
.\venv\Scripts\Activate.ps1
pip install -r fastapi_app/requirements.txt
```

### Lỗi: "Database connection failed"
- Kiểm tra PostgreSQL service đang chạy
- Kiểm tra mật khẩu trong file `.env` đúng chưa
- Kiểm tra database `elearning` đã tồn tại chưa

### Lỗi: "Port already in use"
- Đổi port trong lệnh chạy
- Hoặc tắt process đang dùng port đó

