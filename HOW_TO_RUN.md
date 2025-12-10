# 🚀 Hướng dẫn Chạy Cả 2 Server

## 📋 Yêu cầu:

1. ✅ PostgreSQL đang chạy
2. ✅ Database `elearning` đã được tạo
3. ✅ Virtual environment đã activate
4. ✅ Dependencies đã cài đặt

## 🎯 Cách 1: Dùng Script (Dễ nhất)

### Windows PowerShell:
```powershell
.\start-dev.ps1
```

### Windows CMD:
```cmd
start-dev.bat
```

Script sẽ tự động:
- ✅ Activate venv
- ✅ Chạy Backend FastAPI (port 8001) trong cửa sổ riêng
- ✅ Chạy Frontend React (port 3000) trong cửa sổ riêng
- ✅ Hiển thị URLs để truy cập

## 🎯 Cách 2: Chạy Thủ công (2 Terminal)

### Terminal 1 - Backend (FastAPI):
```powershell
# Từ thư mục root
.\venv\Scripts\Activate.ps1
uvicorn fastapi_app.main:app --reload --port 8001
```

### Terminal 2 - Frontend (React):
```powershell
# Từ thư mục root
cd frontend
npm run dev
```

## 📍 URLs để truy cập:

- **Frontend (React)**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8001
- **API Docs (Swagger)**: http://127.0.0.1:8001/docs
- **Health Check**: http://127.0.0.1:8001/health

## ✅ Kiểm tra Server đang chạy:

### Kiểm tra Backend:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8001/health" -UseBasicParsing
```
→ Sẽ trả về: `{"status":"ok"}`

### Kiểm tra Frontend:
Mở browser: http://localhost:3000

## 🐛 Troubleshooting:

### Backend không chạy được:
1. Kiểm tra PostgreSQL đang chạy:
   ```powershell
   psql -U postgres
   ```

2. Kiểm tra `.env` file:
   ```powershell
   cat fastapi_app\.env
   ```

3. Kiểm tra database connection:
   ```powershell
   psql -U elearn -d elearning
   ```

### Frontend không chạy được:
1. Kiểm tra đã cài dependencies:
   ```powershell
   cd frontend
   npm install
   ```

2. Kiểm tra port 3000 đang được dùng:
   ```powershell
   netstat -ano | findstr :3000
   ```

### Lỗi "Cannot connect to backend":
- Đảm bảo Backend đang chạy ở port 8001
- Kiểm tra CORS settings trong `fastapi_app/main.py`
- Kiểm tra proxy trong `frontend/vite.config.js`

## 🛑 Dừng Server:

### Nếu dùng script:
- Đóng các cửa sổ PowerShell/CMD đã mở

### Nếu chạy thủ công:
- Nhấn `Ctrl+C` trong mỗi terminal

## 📝 Checklist trước khi chạy:

- [ ] PostgreSQL đang chạy
- [ ] Database `elearning` đã tạo
- [ ] Tables đã được tạo (chạy `schema_pg.sql`)
- [ ] File `.env` đã cấu hình đúng
- [ ] Virtual environment đã activate
- [ ] Backend dependencies đã cài (`pip install -r fastapi_app/requirements.txt`)
- [ ] Frontend dependencies đã cài (`cd frontend && npm install`)

## 🎉 Sau khi chạy thành công:

1. Mở browser: http://localhost:3000
2. Đăng ký user mới hoặc đăng nhập
3. Xem danh sách khóa học
4. Click vào khóa học để xem chi tiết
5. Test các tính năng khác

