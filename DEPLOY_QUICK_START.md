# ⚡ Deploy Quick Start - Tóm tắt nhanh

Hướng dẫn nhanh để deploy Code Đơ lên Render (Backend) và Vercel (Frontend).

---

## 🚀 DEPLOY BACKEND (RENDER)

### 1. Tạo Web Service
- Vào: https://dashboard.render.com
- New + → Web Service
- Kết nối GitHub repo

### 2. Cấu hình Build
```
Build Command: pip install -r fastapi_app/requirements.txt
Start Command: cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Environment Variables
| Key | Value |
|-----|-------|
| `DATABASE_URL` | Internal Database URL từ Render (có `+psycopg`) |
| `JWT_SECRET` | Chuỗi ngẫu nhiên dài (32+ ký tự) |
| `JWT_ALG` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `REFRESH_TOKEN_EXPIRE_MINUTES` | `1440` |
| `ALLOWED_ORIGINS` | `["http://localhost:3000"]` (tạm thời) |

### 4. Deploy
- Click "Create Web Service"
- Đợi 5-10 phút
- Lưu URL backend: `https://code-do-backend.onrender.com`

### 5. Kiểm tra
- Truy cập: `https://code-do-backend.onrender.com/docs`
- Thấy Swagger UI → Thành công! ✅

---

## 🎨 DEPLOY FRONTEND (VERCEL)

### 1. Tạo Project
- Vào: https://vercel.com
- Add New → Project
- Import GitHub repo

### 2. Cấu hình
```
Root Directory: frontend
Framework: Vite (tự động detect)
```

### 3. Environment Variables
| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | URL backend từ Render (không có trailing slash) |

### 4. Deploy
- Click "Deploy"
- Đợi 2-5 phút
- Lưu URL frontend: `https://code-do-frontend.vercel.app`

---

## 🔄 CẬP NHẬT CORS

### Sau khi có URL frontend:

1. Vào Render Dashboard → Web Service → Environment
2. Cập nhật `ALLOWED_ORIGINS`:
   ```
   ["https://code-do-frontend.vercel.app"]
   ```
3. Save Changes → Render tự động redeploy

---

## ✅ CHECKLIST

### Backend
- [ ] Database đã tạo và migrations đã chạy
- [ ] Web Service đã tạo
- [ ] Environment Variables đã set đầy đủ
- [ ] Deploy thành công
- [ ] `/docs` endpoint hoạt động

### Frontend
- [ ] Project đã tạo trên Vercel
- [ ] `VITE_API_BASE_URL` đã set
- [ ] Deploy thành công
- [ ] Website load được

### Kết nối
- [ ] `ALLOWED_ORIGINS` đã cập nhật với URL frontend
- [ ] Backend đã redeploy
- [ ] Không có lỗi CORS
- [ ] Đăng nhập/đăng ký hoạt động

---

## 🐛 LỖI THƯỜNG GẶP

**Backend không start:**
- Kiểm tra `DATABASE_URL` (phải có `+psycopg`)
- Kiểm tra Logs trên Render

**CORS Error:**
- Kiểm tra `ALLOWED_ORIGINS` có URL frontend chưa
- Format phải là JSON array: `["https://..."]`

**404 Not Found:**
- Kiểm tra `VITE_API_BASE_URL` có đúng không
- Không có trailing slash

---

## 📚 Tài liệu chi tiết

Xem file `HUONG_DAN_DEPLOY_CHI_TIET.md` để có hướng dẫn từng bước chi tiết hơn.

---

**Chúc bạn deploy thành công! 🎉**
