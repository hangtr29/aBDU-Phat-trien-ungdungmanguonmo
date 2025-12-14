# 🚀 Hướng dẫn chạy dự án Code Đơ

Hướng dẫn từng bước để chạy dự án e-learning.

## 📋 Yêu cầu hệ thống

- ✅ Python 3.8+
- ✅ Node.js 16+
- ✅ PostgreSQL 12+ (đã cài đặt)
- ✅ Git

## 🔧 Bước 1: Kiểm tra và cài đặt dependencies

### 1.1. Kiểm tra Python và Node.js

```powershell
# Kiểm tra Python
python --version

# Kiểm tra Node.js
node --version
npm --version
```

### 1.2. Tạo và kích hoạt virtual environment (nếu chưa có)

```powershell
# Tạo virtual environment (chỉ cần chạy lần đầu)
python -m venv venv

# Kích hoạt virtual environment
.\venv\Scripts\Activate.ps1
```

Bạn sẽ thấy `(venv)` ở đầu dòng lệnh.

### 1.3. Cài đặt Python dependencies

```powershell
# Đảm bảo đang trong virtual environment
pip install -r fastapi_app/requirements.txt
```

### 1.4. Cài đặt Frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

## 🗄️ Bước 2: Setup Database

### 2.1. Kiểm tra PostgreSQL đang chạy

1. Nhấn `Windows + R`, gõ: `services.msc`
2. Tìm service `postgresql-x64-18` (hoặc version của bạn)
3. Đảm bảo service đang **Running**

### 2.2. Chạy migrations (tạo các bảng)

```powershell
.\scripts\setup-all-migrations.ps1
```

Khi được hỏi:
- `Ban co muon tiep tuc? (y/n):` → Nhập `y`
- `Password for user postgres:` → Nhập mật khẩu PostgreSQL của bạn (ví dụ: `mat_khau_moi`)

Script sẽ chạy tất cả migrations và tạo các bảng cần thiết.

### 2.3. Seed dữ liệu (tùy chọn)

Nếu chưa có dữ liệu mẫu, chạy:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -d elearning -f database/seed_programming_courses_fixed_utf8.sql
```

Mật khẩu: `mat_khau_moi` (hoặc mật khẩu của bạn)

## ⚙️ Bước 3: Cấu hình Backend

### 3.1. Tạo file `.env`

Tạo file `fastapi_app/.env` với nội dung sau:

```env
DATABASE_URL=postgresql+psycopg://postgres:mat_khau_moi@localhost:5432/elearning
JWT_SECRET=your-secret-key-here-change-in-production-123456
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Lưu ý quan trọng:**
- Thay `mat_khau_moi` bằng mật khẩu PostgreSQL thực tế của bạn
- Thay `your-secret-key-here-change-in-production-123456` bằng một chuỗi bí mật ngẫu nhiên (cho bảo mật)

## 🚀 Bước 4: Chạy dự án

### Cách 1: Chạy tự động (Khuyến nghị) ⭐

Từ thư mục root của dự án:

```powershell
.\start-dev.ps1
```

Script sẽ:
1. ✅ Activate virtual environment
2. ✅ Cài đặt frontend dependencies (nếu chưa có)
3. ✅ Chạy Backend trong cửa sổ PowerShell mới (port 8001)
4. ✅ Chạy Frontend trong cửa sổ PowerShell mới (port 3000)

**Lưu ý:** Sẽ mở 2 cửa sổ PowerShell mới, đừng đóng chúng!

### Cách 2: Chạy thủ công

Mở **2 terminal riêng biệt**:

#### Terminal 1 - Backend:

```powershell
# Từ thư mục root
.\venv\Scripts\Activate.ps1
uvicorn fastapi_app.main:app --reload --port 8001
```

Bạn sẽ thấy:
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend:

```powershell
# Từ thư mục root
cd frontend
npm run dev
```

Bạn sẽ thấy:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

## 🌐 Bước 5: Truy cập ứng dụng

Sau khi cả 2 server đã chạy:

- **Frontend (Giao diện người dùng):** http://localhost:3000
- **Backend API:** http://127.0.0.1:8001
- **API Documentation (Swagger):** http://127.0.0.1:8001/docs
- **API ReDoc:** http://127.0.0.1:8001/redoc

## 🔐 Bước 6: Đăng nhập

### Tài khoản mặc định (nếu đã seed data):

**Admin:**
- Email: `admin@example.com`
- Password: `admin123`

**Giáo viên:**
- Email: `teacher@example.com`
- Password: `teacher123`

**Học viên:**
- Email: `student@example.com`
- Password: `student123`

Hoặc đăng ký tài khoản mới tại: http://localhost:3000/register

## 🛑 Dừng dự án

### Nếu dùng script tự động:
- Đóng 2 cửa sổ PowerShell đã mở

### Nếu chạy thủ công:
- Nhấn `Ctrl + C` trong mỗi terminal để dừng server

## 🔧 Troubleshooting

### ❌ Lỗi: "Module not found"

```powershell
.\venv\Scripts\Activate.ps1
pip install -r fastapi_app/requirements.txt
```

### ❌ Lỗi: "Database connection failed"

1. **Kiểm tra PostgreSQL service:**
   ```powershell
   # Mở services.msc và kiểm tra postgresql service đang chạy
   ```

2. **Kiểm tra file `.env`:**
   - Đảm bảo `DATABASE_URL` đúng
   - Đảm bảo mật khẩu đúng

3. **Kiểm tra database tồn tại:**
   ```powershell
   & "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -l
   ```
   Tìm database `elearning` trong danh sách

### ❌ Lỗi: "Port already in use"

**Port 8001 (Backend) bị chiếm:**
```powershell
# Tìm process đang dùng port 8001
netstat -ano | findstr :8001

# Kill process (thay PID bằng số từ lệnh trên)
taskkill /PID <PID> /F
```

**Port 3000 (Frontend) bị chiếm:**
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

Hoặc đổi port trong lệnh chạy:
- Backend: `uvicorn fastapi_app.main:app --reload --port 8002`
- Frontend: Sửa `vite.config.js` hoặc dùng `npm run dev -- --port 3001`

### ❌ Lỗi: "Invalid or expired token"

- Đăng nhập lại để lấy token mới
- Token mặc định hết hạn sau 30 phút

### ❌ Lỗi: "npm install failed"

```powershell
# Xóa node_modules và cài lại
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### ❌ Lỗi: "psql: command not found"

Sử dụng đường dẫn đầy đủ:
```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
```

## 📝 Checklist chạy dự án

Trước khi chạy, đảm bảo:

- [ ] PostgreSQL service đang chạy
- [ ] Database `elearning` đã được tạo
- [ ] Đã chạy migrations (tất cả bảng đã được tạo)
- [ ] File `fastapi_app/.env` đã được tạo với đúng cấu hình
- [ ] Virtual environment đã được activate
- [ ] Python dependencies đã được cài đặt
- [ ] Frontend dependencies đã được cài đặt (`npm install`)

## 🎯 Tóm tắt nhanh

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Chạy migrations (nếu chưa chạy)
.\scripts\setup-all-migrations.ps1

# 3. Tạo file .env (nếu chưa có)
# Xem Bước 3.1 ở trên

# 4. Chạy dự án
.\start-dev.ps1
```

Sau đó truy cập: **http://localhost:3000**

## 📞 Cần giúp đỡ?

Nếu gặp lỗi, hãy:
1. Kiểm tra console browser (F12) để xem lỗi frontend
2. Kiểm tra terminal backend để xem lỗi server
3. Kiểm tra file `.env` có đúng cấu hình không
4. Đảm bảo PostgreSQL service đang chạy

---

**Chúc bạn code vui vẻ! 🎉**

