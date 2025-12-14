# ⚡ Deploy Quick Start - Code Đơ

Hướng dẫn nhanh để deploy trong 10 phút.

## 🗄️ BACKEND - RENDER (5 phút)

### 1. Tạo Web Service
- Vào: https://dashboard.render.com
- **New +** → **Web Service**
- Connect GitHub repo

### 2. Cấu hình
- **Name**: `code-do-backend`
- **Build Command**: `pip install -r fastapi_app/requirements.txt`
- **Start Command**: `cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables
```
DATABASE_URL = postgresql+psycopg://code_do_user:AhJhY0xzA5hDDFLc8VvThh1dE3RiGXbs@dpg-d4v7vl3e5dus73a8sqtg-a/elearning_r201
JWT_SECRET = your-super-secret-key-here
JWT_ALG = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440
ALLOWED_ORIGINS = ["http://localhost:3000"]
```

### 4. Deploy
- Click **Create Web Service**
- Đợi 5-10 phút
- Lưu URL: `https://code-do-backend.onrender.com`

---

## 🎨 FRONTEND - VERCEL (5 phút)

### 1. Tạo Project
- Vào: https://vercel.com
- **New Project**
- Import GitHub repo

### 2. Cấu hình
- **Root Directory**: `frontend`
- **Framework**: Vite (auto-detect)

### 3. Environment Variables
```
VITE_API_BASE_URL = https://code-do-backend.onrender.com
```

### 4. Deploy
- Click **Deploy**
- Đợi 2-5 phút
- Lưu URL: `https://code-do-frontend.vercel.app`

### 5. Cập nhật CORS
- Vào Render → Web Service → Environment
- Cập nhật `ALLOWED_ORIGINS`:
  ```
  ["https://code-do-frontend.vercel.app"]
  ```

---

## ✅ KIỂM TRA

1. **Backend**: `https://code-do-backend.onrender.com/docs`
2. **Frontend**: `https://code-do-frontend.vercel.app`
3. **Test**: Đăng ký/đăng nhập

---

## 📖 Chi tiết đầy đủ

Xem file: `HUONG_DAN_DEPLOY_CHI_TIET.md`

