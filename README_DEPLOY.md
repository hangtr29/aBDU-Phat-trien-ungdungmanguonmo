# 🚀 Hướng dẫn Deploy Code Đơ

## 📚 Tài liệu

- **HUONG_DAN_DEPLOY.md** - Hướng dẫn deploy chi tiết từng bước
- **DEPLOY_CHECKLIST.md** - Checklist kiểm tra trước khi deploy

## ⚡ Quick Start

### 1. Backend trên Render

1. Tạo PostgreSQL database trên Render
2. Tạo Web Service, kết nối GitHub repo
3. Cấu hình:
   - **Build Command**: `pip install -r fastapi_app/requirements.txt`
   - **Start Command**: `cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variables (xem chi tiết trong HUONG_DAN_DEPLOY.md)
5. Chạy migrations: `python scripts/run_migrations.py`

### 2. Frontend trên Vercel

1. Import GitHub repo vào Vercel
2. Cấu hình:
   - **Root Directory**: `frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
3. Set Environment Variable:
   - `VITE_API_BASE_URL` = URL backend từ Render
4. Deploy!

### 3. Cập nhật CORS

Sau khi có URL frontend, cập nhật `ALLOWED_ORIGINS` trên Render:
```
["https://your-frontend.vercel.app"]
```

## 📝 Lưu ý quan trọng

1. **DATABASE_URL**: Dùng Internal Database URL (không phải External)
2. **JWT_SECRET**: Phải là chuỗi ngẫu nhiên dài và phức tạp
3. **ALLOWED_ORIGINS**: Format JSON array, ví dụ: `["https://example.com"]`
4. **VITE_API_BASE_URL**: Phải có `https://`, không có trailing slash

## 🔗 Links hữu ích

- Render Dashboard: https://dashboard.render.com
- Vercel Dashboard: https://vercel.com/dashboard
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs

---

Xem **HUONG_DAN_DEPLOY.md** để biết chi tiết từng bước!

