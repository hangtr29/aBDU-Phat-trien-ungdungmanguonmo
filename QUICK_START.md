# 🚀 Quick Start Guide

## ✅ Server đã chạy thành công!

Khi bạn thấy `{"detail":"Not Found"}` ở `http://127.0.0.1:8001` → **Đây là bình thường!**

FastAPI là API backend, không có route cho root path `/`.

## 📍 Các URL quan trọng:

### 1. **Swagger UI (API Documentation)**
```
http://127.0.0.1:8001/docs
```
→ Đây là nơi bạn test tất cả API endpoints!

### 2. **Health Check**
```
http://127.0.0.1:8001/health
```
→ Sẽ trả về: `{"status":"ok"}`

### 3. **API Endpoints chính:**

#### Authentication
- `POST /api/auth/register` - Đăng ký
- `POST /api/auth/login` - Đăng nhập (nhận JWT token)

#### Courses
- `GET /api/courses` - Danh sách khóa học
- `GET /api/courses/{id}` - Chi tiết khóa học
- `POST /api/courses` - Tạo khóa học (cần token)

#### Lessons
- `GET /api/courses/{id}/lessons` - Danh sách bài học
- `POST /api/courses/{id}/lessons` - Tạo bài học (cần token)

#### Progress
- `GET /api/courses/{id}/progress` - Lấy tiến độ
- `POST /api/courses/{id}/progress` - Cập nhật tiến độ

#### Certificates
- `GET /api/courses/{id}/certificate` - Lấy chứng nhận

#### Discussions
- `GET /api/courses/{id}/discussions` - Danh sách thảo luận
- `POST /api/courses/{id}/discussions` - Tạo thảo luận

## 🧪 Cách test API:

### Bước 1: Mở Swagger UI
```
http://127.0.0.1:8001/docs
```

### Bước 2: Đăng ký user mới
1. Tìm `POST /api/auth/register`
2. Click "Try it out"
3. Nhập thông tin:
```json
{
  "email": "test@example.com",
  "password": "test123",
  "ho_ten": "Nguyen Van Test",
  "so_dien_thoai": "0123456789"
}
```
4. Click "Execute"
5. Copy `access_token` từ response

### Bước 3: Authorize với token
1. Click nút **"Authorize"** ở góc trên bên phải
2. Dán token vào ô "Value"
3. Click "Authorize" → "Close"

### Bước 4: Test các API khác
Bây giờ bạn có thể test các API cần authentication!

## 🎨 Chạy Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

## 📝 Lưu ý:

- Root path `/` trả về "Not Found" → **Bình thường!**
- Luôn dùng `/docs` để xem và test API
- Frontend sẽ tự động kết nối với backend qua proxy

