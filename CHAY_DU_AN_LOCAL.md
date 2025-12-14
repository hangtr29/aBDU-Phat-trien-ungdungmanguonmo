# 🚀 Hướng dẫn chạy dự án Local (Đơn giản)

Hướng dẫn nhanh để chạy dự án trên máy local.

## 📋 Yêu cầu

- ✅ Python 3.8+ (đã cài)
- ✅ Node.js 16+ (đã cài)
- ✅ PostgreSQL (đã cài và đang chạy)
- ✅ Đã có database `elearning` và đã chạy migrations

## ⚡ Cách chạy nhanh (3 bước)

### Bước 1: Cấu hình Backend

Tạo file `fastapi_app/.env` với nội dung:

```env
DATABASE_URL=postgresql+psycopg://postgres:MAT_KHAU_POSTGRES@localhost:5432/elearning
JWT_SECRET=your-secret-key-here-change-in-production-123456
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Lưu ý:** Thay `MAT_KHAU_POSTGRES` bằng mật khẩu PostgreSQL thực tế của bạn.

### Bước 2: Cấu hình Frontend

Tạo file `frontend/.env` với nội dung:

```env
VITE_API_BASE_URL=http://127.0.0.1:8001
```

### Bước 3: Chạy dự án

**Cách 1: Dùng script tự động (Khuyến nghị) ⭐**

Từ thư mục root của dự án:

```powershell
.\start-dev.ps1
```

Script sẽ tự động:
- ✅ Activate virtual environment
- ✅ Chạy Backend (port 8001) trong cửa sổ PowerShell mới
- ✅ Chạy Frontend (port 3000) trong cửa sổ PowerShell mới

**Cách 2: Chạy thủ công**

Mở **2 terminal riêng biệt**:

**Terminal 1 - Backend:**
```powershell
# Từ thư mục root
.\venv\Scripts\Activate.ps1
uvicorn fastapi_app.main:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```powershell
# Từ thư mục root
cd frontend
npm run dev
```

## 🌐 Truy cập ứng dụng

Sau khi cả 2 server đã chạy:

- **Frontend:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8001
- **API Docs (Swagger):** http://127.0.0.1:8001/docs

## 🔐 Đăng nhập

Tài khoản test (nếu đã seed data):

- **Student:**
  - Email: `student@example.com`
  - Password: `student123`

- **Teacher:**
  - Email: `teacher1@example.com`
  - Password: `teacher123`

- **Admin:**
  - Email: `admin@example.com`
  - Password: `admin123`

## 🛑 Dừng dự án

- **Nếu dùng script:** Đóng 2 cửa sổ PowerShell đã mở
- **Nếu chạy thủ công:** Nhấn `Ctrl + C` trong mỗi terminal

## 🔧 Troubleshooting

### ❌ Lỗi: "Module not found"

```powershell
.\venv\Scripts\Activate.ps1
pip install -r fastapi_app/requirements.txt
```

### ❌ Lỗi: "Database connection failed"

1. Kiểm tra PostgreSQL service đang chạy:
   - Nhấn `Windows + R`, gõ: `services.msc`
   - Tìm `postgresql-x64-18` → Đảm bảo đang **Running**

2. Kiểm tra file `.env`:
   - `DATABASE_URL` đúng format
   - Mật khẩu PostgreSQL đúng

### ❌ Lỗi: "Port already in use"

**Port 8001 (Backend) bị chiếm:**
```powershell
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

**Port 3000 (Frontend) bị chiếm:**
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### ❌ Lỗi: "npm install failed"

```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### ❌ Lỗi: "CORS policy"

Đảm bảo `ALLOWED_ORIGINS` trong `fastapi_app/.env` có:
```
ALLOWED_ORIGINS=["http://localhost:3000"]
```

## 📝 Checklist

Trước khi chạy, đảm bảo:

- [ ] PostgreSQL service đang chạy
- [ ] Database `elearning` đã được tạo
- [ ] Đã chạy migrations (tất cả bảng đã được tạo)
- [ ] File `fastapi_app/.env` đã được tạo với đúng cấu hình
- [ ] File `frontend/.env` đã được tạo với `VITE_API_BASE_URL`
- [ ] Virtual environment đã được activate
- [ ] Python dependencies đã được cài đặt
- [ ] Frontend dependencies đã được cài đặt

## 🎯 Tóm tắt nhanh

```powershell
# 1. Tạo file fastapi_app/.env (xem Bước 1)
# 2. Tạo file frontend/.env (xem Bước 2)
# 3. Chạy dự án
.\start-dev.ps1
```

Sau đó truy cập: **http://localhost:3000**

---

**Chúc bạn code vui vẻ! 🎉**

