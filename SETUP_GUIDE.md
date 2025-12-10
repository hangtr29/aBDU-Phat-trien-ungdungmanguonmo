# Hướng dẫn Setup và Chạy Project

## 📋 Tổng quan

Project gồm 2 phần:
- **Backend**: FastAPI + PostgreSQL + JWT (`fastapi_app/`)
- **Frontend**: React + Vite (`frontend/`)

## 🚀 Backend Setup

### 1. Cài đặt dependencies

```bash
cd fastapi_app
pip install -r requirements.txt
```

### 2. Cấu hình database

Đảm bảo PostgreSQL đang chạy và tạo file `.env`:

```env
DATABASE_URL=postgresql+psycopg://elearn:password@localhost:5432/elearning
JWT_SECRET=your-secret-key-here
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Chạy migrations (tạo tables)

```bash
# Từ thư mục database/
psql -U elearn -d elearning -f schema_pg.sql
```

### 4. Seed data (tùy chọn)

```bash
psql -U elearn -d elearning -f seed_courses.sql
```

### 5. Chạy server

**QUAN TRỌNG**: Phải chạy từ thư mục **root** (không phải từ trong `fastapi_app`):

```bash
# Từ thư mục root của project
uvicorn fastapi_app.main:app --reload --port 8001
```

Hoặc dùng script có sẵn:
```bash
# Windows PowerShell
.\fastapi_app\run.ps1

# Windows CMD
.\fastapi_app\run.bat
```

Backend sẽ chạy tại: `http://127.0.0.1:8001`
API docs: `http://127.0.0.1:8001/docs`

## 🎨 Frontend Setup

### 1. Cài đặt dependencies

```bash
cd frontend
npm install
```

### 2. Chạy development server

```bash
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

## ✅ Checklist đã hoàn thành

### Backend APIs
- ✅ POST `/api/auth/register` - Đăng ký
- ✅ POST `/api/auth/login` - Đăng nhập (JWT)
- ✅ GET `/api/users/me` - Thông tin user
- ✅ GET `/api/courses` - Danh sách khóa học
- ✅ GET `/api/courses/{id}` - Chi tiết khóa học
- ✅ POST `/api/courses` - Tạo khóa học
- ✅ GET `/api/courses/{id}/lessons` - Danh sách bài học
- ✅ POST `/api/courses/{id}/lessons` - Tạo bài học (với file upload)
- ✅ POST `/api/courses/{id}/progress` - Cập nhật progress
- ✅ GET `/api/courses/{id}/progress` - Lấy progress
- ✅ GET `/api/courses/{id}/certificate` - Lấy certificate
- ✅ POST `/api/courses/{id}/complete` - Hoàn thành khóa học
- ✅ GET `/api/courses/{id}/discussions` - Danh sách thảo luận
- ✅ POST `/api/courses/{id}/discussions` - Tạo thảo luận

### Frontend Pages
- ✅ Login/Register với JWT
- ✅ Danh sách khóa học
- ✅ Chi tiết khóa học với Lesson Tree
- ✅ Video Player (YouTube, Vimeo, HTML5)
- ✅ Drip Content (locked/unlocked)

## 🔄 Cần bổ sung

### Frontend
- [ ] Progress Tracking UI
- [ ] File Upload form cho giáo viên
- [ ] Certificates page
- [ ] Discussion Forum UI
- [ ] Video streaming optimization

### Backend
- [ ] Video streaming endpoint
- [ ] File upload validation
- [ ] Email notifications
- [ ] Admin dashboard APIs

## 📝 Testing

### Test Backend APIs

1. Mở `http://127.0.0.1:8001/docs`
2. Đăng ký user mới: `POST /api/auth/register`
3. Đăng nhập: `POST /api/auth/login` → Copy `access_token`
4. Click "Authorize" → Dán token vào ô Bearer
5. Test các endpoints khác

### Test Frontend

1. Chạy cả backend và frontend
2. Mở `http://localhost:3000`
3. Đăng ký/Đăng nhập
4. Xem danh sách khóa học
5. Click vào khóa học để xem chi tiết và video

## 🐛 Troubleshooting

### Backend không kết nối được database
- Kiểm tra PostgreSQL đang chạy: `psql -U postgres`
- Kiểm tra `.env` file có đúng `DATABASE_URL` không
- Kiểm tra user `elearn` có quyền truy cập database `elearning`

### Frontend không gọi được API
- Kiểm tra backend đang chạy tại port 8001
- Kiểm tra proxy trong `vite.config.js`
- Kiểm tra CORS settings trong `fastapi_app/main.py`

### Lỗi import modules
- Đảm bảo đang ở đúng thư mục khi chạy lệnh
- Kiểm tra virtual environment đã activate chưa
- Chạy `pip install -r requirements.txt` lại

