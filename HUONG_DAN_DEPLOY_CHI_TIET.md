# 🚀 Hướng dẫn Deploy Chi Tiết - Code Đơ

Hướng dẫn từng bước cụ thể để deploy backend lên Render và frontend lên Vercel.

---

## 📋 CHUẨN BỊ

✅ **Đã hoàn thành:**
- [x] Code đã được push lên GitHub
- [x] Database migrations đã chạy trên Render
- [x] Có tài khoản Render (miễn phí): https://render.com
- [x] Có tài khoản Vercel (miễn phí): https://vercel.com

---

## 🗄️ PHẦN 1: DEPLOY BACKEND LÊN RENDER

### Bước 1.1: Tạo Web Service trên Render

1. **Đăng nhập Render:**
   - Vào: https://dashboard.render.com
   - Đăng nhập bằng GitHub (khuyến nghị)

2. **Tạo Web Service:**
   - Click nút **"New +"** (góc trên bên phải)
   - Chọn **"Web Service"**

3. **Kết nối GitHub:**
   - Nếu chưa kết nối, click **"Connect account"**
   - Chọn repository: `BDU-Phat-trien-ungdungmanguonmo` (hoặc tên repo của bạn)
   - Click **"Connect"**

4. **Cấu hình cơ bản:**
   - **Name**: `code-do-backend` (hoặc tên bạn muốn)
   - **Region**: Chọn gần nhất (Singapore hoặc US)
   - **Branch**: `main`
   - **Root Directory**: Để **TRỐNG** (không điền gì)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r fastapi_app/requirements.txt
     ```
   - **Start Command**: 
     ```bash
     cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

### Bước 1.2: Cấu hình Environment Variables

1. **Scroll xuống phần "Environment Variables"**

2. **Thêm các biến sau (click "Add Environment Variable" cho mỗi biến):**

   | Key | Value | Ghi chú |
   |-----|-------|---------|
   | `DATABASE_URL` | `postgresql+psycopg://code_do_user:AhJhY0xzA5hDDFLc8VvThh1dE3RiGXbs@dpg-d4v7vl3e5dus73a8sqtg-a/elearning_r201` | **Internal Database URL** (không có hostname đầy đủ) |
   | `JWT_SECRET` | `your-super-secret-key-change-this-to-random-string-123456789` | Tạo chuỗi ngẫu nhiên dài (ít nhất 32 ký tự) |
   | `JWT_ALG` | `HS256` | |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | |
   | `REFRESH_TOKEN_EXPIRE_MINUTES` | `1440` | |
   | `ALLOWED_ORIGINS` | `["http://localhost:3000"]` | **Tạm thời**, sẽ cập nhật sau khi deploy frontend |

   **⚠️ QUAN TRỌNG:**
   - `DATABASE_URL`: Phải dùng **Internal Database URL** (format: `postgresql+psycopg://user:pass@dpg-xxxxx-a/database`)
   - `JWT_SECRET`: Tạo một chuỗi ngẫu nhiên dài và phức tạp (có thể dùng: https://randomkeygen.com/)
   - `ALLOWED_ORIGINS`: Tạm thời để localhost, sau khi có URL frontend sẽ cập nhật

### Bước 1.3: Deploy Backend

1. **Click nút "Create Web Service"** (màu xanh, góc dưới bên phải)

2. **Đợi build:**
   - Render sẽ tự động:
     - Clone code từ GitHub
     - Chạy Build Command
     - Start service
   - Thời gian: **5-10 phút**

3. **Kiểm tra logs:**
   - Scroll xuống phần "Logs"
   - Xem quá trình build
   - Nếu có lỗi, sẽ hiển thị ở đây

4. **Lưu URL backend:**
   - Khi deploy xong, Render sẽ cung cấp URL: `https://code-do-backend.onrender.com`
   - **Copy URL này** để dùng cho frontend

### Bước 1.4: Kiểm tra Backend

1. **Truy cập Swagger UI:**
   - Mở: `https://code-do-backend.onrender.com/docs`
   - Nếu thấy Swagger UI → Backend đã chạy thành công ✅

2. **Test API:**
   - Click thử một endpoint (ví dụ: `GET /api/users/me`)
   - Xem response

---

## 🎨 PHẦN 2: DEPLOY FRONTEND LÊN VERCEL

### Bước 2.1: Tạo Project trên Vercel

1. **Đăng nhập Vercel:**
   - Vào: https://vercel.com
   - Đăng nhập bằng GitHub (khuyến nghị)

2. **Tạo Project mới:**
   - Click **"Add New..."** → **"Project"**
   - Hoặc vào Dashboard → **"New Project"**

3. **Import Repository:**
   - Tìm repository: `BDU-Phat-trien-ungdungmanguonmo` (hoặc tên repo của bạn)
   - Click **"Import"**

### Bước 2.2: Cấu hình Build Settings

Vercel sẽ tự động detect Vite, nhưng cần kiểm tra:

1. **Framework Preset:**
   - Chọn: **"Vite"** (hoặc để Vercel tự detect)

2. **Root Directory:**
   - Click **"Edit"** → **"Root Directory"**
   - Chọn: **`frontend`**
   - Click **"Continue"**

3. **Build Settings (tự động, nhưng kiểm tra):**
   - **Build Command**: `npm run build` (hoặc `cd frontend && npm run build`)
   - **Output Directory**: `dist` (hoặc `frontend/dist`)
   - **Install Command**: `npm install` (hoặc `cd frontend && npm install`)

### Bước 2.3: Cấu hình Environment Variables

1. **Scroll xuống phần "Environment Variables"**

2. **Thêm biến:**
   - Click **"Add"** hoặc **"Add Environment Variable"**
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://code-do-backend.onrender.com` (URL backend từ Render)
   - **Environment**: Chọn tất cả (Production, Preview, Development)
   - Click **"Save"**

   **⚠️ LƯU Ý:**
   - URL backend phải có `https://` (không có trailing slash `/`)
   - Vercel yêu cầu prefix `VITE_` cho các biến môi trường

### Bước 2.4: Deploy Frontend

1. **Click nút "Deploy"** (màu xanh, góc dưới bên phải)

2. **Đợi build:**
   - Vercel sẽ tự động:
     - Install dependencies
     - Build project
     - Deploy
   - Thời gian: **2-5 phút**

3. **Lưu URL frontend:**
   - Khi deploy xong, Vercel sẽ cung cấp URL: `https://code-do-frontend.vercel.app` (hoặc tên bạn đặt)
   - **Copy URL này** để cập nhật CORS trên backend

### Bước 2.5: Cập nhật CORS trên Backend

1. **Vào Render Dashboard:**
   - Chọn Web Service: `code-do-backend`
   - Click tab **"Environment"**

2. **Cập nhật `ALLOWED_ORIGINS`:**
   - Tìm biến `ALLOWED_ORIGINS`
   - Click **"Edit"** (icon bút chì)
   - Thay đổi giá trị thành:
     ```
     ["https://code-do-frontend.vercel.app"]
     ```
   - **Lưu ý:** Thay `code-do-frontend.vercel.app` bằng URL frontend thực tế của bạn
   - Click **"Save Changes"**

3. **Render sẽ tự động redeploy:**
   - Đợi 1-2 phút để redeploy xong

---

## ✅ PHẦN 3: KIỂM TRA VÀ TEST

### Bước 3.1: Test Backend

1. **Truy cập Swagger UI:**
   - URL: `https://code-do-backend.onrender.com/docs`
   - Kiểm tra có hiển thị không

2. **Test một endpoint:**
   - Thử `GET /api/health` hoặc `GET /api/users/me`
   - Xem response

### Bước 3.2: Test Frontend

1. **Truy cập website:**
   - URL: `https://code-do-frontend.vercel.app`
   - Kiểm tra trang chủ có load không

2. **Test đăng ký/đăng nhập:**
   - Thử đăng ký tài khoản mới
   - Thử đăng nhập
   - Kiểm tra có lỗi không

3. **Test các chức năng:**
   - Xem khóa học
   - Đăng ký khóa học
   - Xem video
   - Nộp bài tập

### Bước 3.3: Kiểm tra Console (nếu có lỗi)

1. **Mở Browser Console:**
   - Nhấn `F12` hoặc `Ctrl+Shift+I`
   - Tab **"Console"**

2. **Kiểm tra lỗi:**
   - Nếu có lỗi CORS → Kiểm tra `ALLOWED_ORIGINS` trên Render
   - Nếu có lỗi 404 → Kiểm tra `VITE_API_BASE_URL` trên Vercel
   - Nếu có lỗi network → Kiểm tra URL backend có đúng không

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### ❌ Backend không start được

**Lỗi:** `ModuleNotFoundError: No module named 'xxx'`

**Giải pháp:**
1. Kiểm tra `fastapi_app/requirements.txt` có đầy đủ dependencies không
2. Xem logs trên Render để biết module nào thiếu
3. Thêm vào `requirements.txt` và commit lại

**Lỗi:** `Database connection failed`

**Giải pháp:**
1. Kiểm tra `DATABASE_URL` trên Render:
   - Phải dùng **Internal Database URL** (không có hostname đầy đủ)
   - Format: `postgresql+psycopg://user:pass@dpg-xxxxx-a/database`
2. Kiểm tra database đã được tạo chưa
3. Kiểm tra migrations đã chạy chưa

### ❌ Frontend không kết nối được Backend

**Lỗi:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Giải pháp:**
1. Vào Render → Web Service → Environment
2. Kiểm tra `ALLOWED_ORIGINS` đã có URL frontend chưa
3. Đảm bảo URL không có trailing slash `/`
4. Format: `["https://your-frontend.vercel.app"]`

**Lỗi:** `404 Not Found` khi gọi API

**Giải pháp:**
1. Kiểm tra `VITE_API_BASE_URL` trên Vercel:
   - Phải có `https://`
   - Không có trailing slash `/`
   - Ví dụ: `https://code-do-backend.onrender.com`
2. Vào Vercel → Project → Settings → Environment Variables
3. Cập nhật và redeploy

**Lỗi:** `Network Error` hoặc `Failed to fetch`

**Giải pháp:**
1. Kiểm tra URL backend có đúng không
2. Kiểm tra backend có đang chạy không (truy cập `/docs`)
3. Kiểm tra browser console để xem lỗi cụ thể

### ❌ Database migrations chưa chạy

**Giải pháp:**
1. Vào Render Dashboard → Database
2. Click tab **"Connect"**
3. Click **"Connect via psql"** → Mở Render Shell
4. Chạy migrations thủ công hoặc dùng script:
   ```bash
   # Từ máy local
   .\scripts\run_migrations_render.ps1 -DatabaseUrl "postgresql://..."
   ```

---

## 📝 CHECKLIST HOÀN THÀNH

### Backend (Render)
- [ ] Đã tạo Web Service trên Render
- [ ] Đã cấu hình đúng Build Command và Start Command
- [ ] Đã set đầy đủ Environment Variables (DATABASE_URL, JWT_SECRET, ...)
- [ ] Backend đã deploy thành công
- [ ] Có thể truy cập `/docs` endpoint
- [ ] Database migrations đã chạy

### Frontend (Vercel)
- [ ] Đã import repository vào Vercel
- [ ] Đã cấu hình đúng Root Directory (`frontend`)
- [ ] Đã set `VITE_API_BASE_URL` environment variable
- [ ] Frontend đã deploy thành công
- [ ] Đã cập nhật `ALLOWED_ORIGINS` trên backend với URL frontend

### Testing
- [ ] Backend API hoạt động (test qua `/docs`)
- [ ] Frontend có thể kết nối với backend
- [ ] Đăng ký/đăng nhập hoạt động
- [ ] Các chức năng chính hoạt động bình thường
- [ ] Không có lỗi CORS
- [ ] Không có lỗi trong browser console

---

## 🔐 LƯU Ý BẢO MẬT

1. **JWT_SECRET:**
   - Phải là chuỗi ngẫu nhiên dài và phức tạp
   - Không được share với ai
   - Có thể tạo tại: https://randomkeygen.com/

2. **DATABASE_URL:**
   - Không được commit vào git
   - Chỉ set trong Environment Variables trên Render

3. **ALLOWED_ORIGINS:**
   - Chỉ cho phép domain frontend của bạn
   - Không thêm `*` (wildcard) trong production

---

## 📞 CẦN GIÚP ĐỠ?

Nếu gặp lỗi:

1. **Kiểm tra logs:**
   - Render: Dashboard → Web Service → Logs
   - Vercel: Dashboard → Project → Deployments → Click deployment → View Logs

2. **Kiểm tra browser console:**
   - Nhấn `F12` → Tab Console
   - Xem lỗi cụ thể

3. **Kiểm tra Network tab:**
   - Nhấn `F12` → Tab Network
   - Xem các API calls có thành công không

---

## 🎉 HOÀN THÀNH!

Sau khi hoàn thành tất cả các bước trên, bạn đã có:
- ✅ Backend chạy trên Render
- ✅ Frontend chạy trên Vercel
- ✅ Database PostgreSQL trên Render
- ✅ Website hoạt động đầy đủ!

**Chúc mừng! Dự án của bạn đã được deploy thành công! 🚀**


Hướng dẫn deploy backend lên **Render** và frontend lên **Vercel** với các bước cụ thể.

---

## 📋 Chuẩn bị

✅ Đảm bảo bạn đã:
- [x] Push toàn bộ code lên GitHub
- [x] Có tài khoản GitHub
- [x] Đã tạo PostgreSQL database trên Render (theo hướng dẫn trước)
- [x] Đã chạy migrations trên database

---

## 🗄️ PHẦN 1: DEPLOY BACKEND LÊN RENDER

### Bước 1.1: Đăng nhập Render

1. Truy cập: https://dashboard.render.com
2. Đăng nhập bằng GitHub (khuyến nghị) hoặc email

### Bước 1.2: Tạo Web Service

1. Click nút **"New +"** ở góc trên bên phải
2. Chọn **"Web Service"**

### Bước 1.3: Kết nối GitHub Repository

1. Nếu chưa kết nối GitHub:
   - Click **"Connect GitHub"**
   - Authorize Render truy cập repository
   - Chọn repository: `BDU-Phat-trien-ungdungmanguonmo` (hoặc tên repo của bạn)

2. Chọn repository và branch:
   - **Repository**: Chọn repo của bạn
   - **Branch**: `main` (hoặc branch bạn muốn deploy)

3. Click **"Continue"**

### Bước 1.4: Cấu hình Build Settings

Điền thông tin sau:

| Field | Value |
|-------|-------|
| **Name** | `code-do-backend` (hoặc tên bạn muốn) |
| **Region** | Chọn gần nhất (Singapore, US, etc.) |
| **Branch** | `main` |
| **Root Directory** | Để trống (hoặc `fastapi_app` nếu cần) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r fastapi_app/requirements.txt` |
| **Start Command** | `cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port $PORT` |

**Lưu ý:** 
- Render tự động set `$PORT`, không cần thay đổi
- Build Command và Start Command phải chính xác như trên

### Bước 1.5: Cấu hình Environment Variables

1. Scroll xuống phần **"Environment Variables"**
2. Click **"Add Environment Variable"** và thêm từng biến sau:

#### Biến 1: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: Dán **Internal Database URL** từ Render Database
  - Format: `postgresql+psycopg://user:pass@dpg-xxxxx-a/database`
  - **LƯU Ý**: Phải có `+psycopg` sau `postgresql`
  - Copy từ Render Database Dashboard → Tab "Info" → "Internal Database URL"

#### Biến 2: JWT_SECRET
- **Key**: `JWT_SECRET`
- **Value**: Tạo một chuỗi ngẫu nhiên dài (ít nhất 32 ký tự)
  - Ví dụ: `my-super-secret-jwt-key-1234567890-abcdefghijklmnopqrstuvwxyz`
  - Hoặc dùng: https://randomkeygen.com/ (chọn "CodeIgniter Encryption Keys")

#### Biến 3: JWT_ALG
- **Key**: `JWT_ALG`
- **Value**: `HS256`

#### Biến 4: ACCESS_TOKEN_EXPIRE_MINUTES
- **Key**: `ACCESS_TOKEN_EXPIRE_MINUTES`
- **Value**: `30`

#### Biến 5: REFRESH_TOKEN_EXPIRE_MINUTES
- **Key**: `REFRESH_TOKEN_EXPIRE_MINUTES`
- **Value**: `1440`

#### Biến 6: ALLOWED_ORIGINS
- **Key**: `ALLOWED_ORIGINS`
- **Value**: `["http://localhost:3000"]` (tạm thời, sẽ cập nhật sau khi deploy frontend)

**Lưu ý quan trọng:**
- `ALLOWED_ORIGINS` phải là JSON array format
- Tạm thời để localhost, sau khi có URL frontend sẽ cập nhật lại

### Bước 1.6: Deploy

1. Scroll xuống cuối trang
2. Click **"Create Web Service"**
3. Render sẽ bắt đầu build và deploy
4. Đợi 5-10 phút để build hoàn tất
5. Khi deploy thành công, bạn sẽ thấy:
   - Status: **"Live"** (màu xanh)
   - URL backend: `https://code-do-backend.onrender.com` (hoặc tên bạn đặt)

### Bước 1.7: Kiểm tra Backend

1. Truy cập: `https://code-do-backend.onrender.com/docs`
2. Bạn sẽ thấy Swagger UI với tất cả API endpoints
3. Nếu thấy Swagger UI → Backend đã deploy thành công! ✅

### Bước 1.8: Xử lý lỗi (nếu có)

**Lỗi Build Failed:**
- Vào **"Logs"** tab để xem lỗi chi tiết
- Kiểm tra `requirements.txt` có đầy đủ dependencies không
- Kiểm tra Build Command có đúng không

**Lỗi Database Connection:**
- Kiểm tra `DATABASE_URL` đã đúng chưa
- Đảm bảo dùng **Internal Database URL** (không phải External)
- Kiểm tra database đã được tạo và migrations đã chạy chưa

**Lỗi Module Not Found:**
- Kiểm tra `fastapi_app/requirements.txt` có đầy đủ packages không
- Kiểm tra Root Directory có đúng không

---

## 🎨 PHẦN 2: DEPLOY FRONTEND LÊN VERCEL

### Bước 2.1: Đăng nhập Vercel

1. Truy cập: https://vercel.com
2. Click **"Sign Up"** hoặc **"Log In"**
3. Chọn **"Continue with GitHub"** (khuyến nghị)

### Bước 2.2: Tạo Project mới

1. Sau khi đăng nhập, bạn sẽ thấy Dashboard
2. Click **"Add New..."** → **"Project"**

### Bước 2.3: Import GitHub Repository

1. Vercel sẽ hiển thị danh sách repositories
2. Tìm và chọn repository của bạn: `BDU-Phat-trien-ungdungmanguonmo`
3. Click **"Import"**

### Bước 2.4: Cấu hình Project Settings

Vercel sẽ tự động detect Vite, nhưng cần kiểm tra:

| Field | Value |
|-------|-------|
| **Project Name** | `code-do-frontend` (hoặc tên bạn muốn) |
| **Framework Preset** | `Vite` (tự động detect) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (hoặc để Vercel tự detect) |
| **Output Directory** | `dist` |
| **Install Command** | `npm install` |

**Lưu ý:**
- Nếu Root Directory là `frontend`, Vercel sẽ tự động chạy commands trong thư mục đó
- Nếu không có Root Directory, cần set Build Command: `cd frontend && npm install && npm run build`

### Bước 2.5: Cấu hình Environment Variables

1. Scroll xuống phần **"Environment Variables"**
2. Click **"Add"** và thêm:

#### Biến: VITE_API_BASE_URL
- **Key**: `VITE_API_BASE_URL`
- **Value**: URL backend từ Render (bước 1.6)
  - Ví dụ: `https://code-do-backend.onrender.com`
  - **LƯU Ý**: 
    - Không có trailing slash (`/`) ở cuối
    - Phải có `https://`
    - Không có `/api` ở cuối (nếu backend không có prefix)

**Lưu ý quan trọng:**
- Vercel yêu cầu prefix `VITE_` cho các biến môi trường
- Sau khi thêm biến, cần rebuild để áp dụng

### Bước 2.6: Deploy

1. Scroll xuống cuối trang
2. Click **"Deploy"**
3. Vercel sẽ bắt đầu build
4. Đợi 2-5 phút để build hoàn tất
5. Khi deploy thành công, bạn sẽ thấy:
   - Status: **"Ready"** (màu xanh)
   - URL frontend: `https://code-do-frontend.vercel.app` (hoặc tên bạn đặt)

### Bước 2.7: Kiểm tra Frontend

1. Truy cập URL frontend: `https://code-do-frontend.vercel.app`
2. Kiểm tra trang web có load được không
3. Mở Developer Tools (F12) → Console tab
4. Kiểm tra có lỗi CORS hoặc API connection không

---

## 🔄 PHẦN 3: CẬP NHẬT CORS VÀ KẾT NỐI

### Bước 3.1: Cập nhật ALLOWED_ORIGINS trên Render

Sau khi có URL frontend từ Vercel:

1. Vào **Render Dashboard** → Chọn Web Service của bạn
2. Vào tab **"Environment"**
3. Tìm biến `ALLOWED_ORIGINS`
4. Click **"Edit"** hoặc **"Update"**
5. Thay đổi value thành:
   ```
   ["https://code-do-frontend.vercel.app"]
   ```
   (Thay bằng URL frontend thực tế của bạn)

6. Click **"Save Changes"**
7. Render sẽ tự động redeploy (đợi 2-3 phút)

### Bước 3.2: Rebuild Frontend (nếu cần)

Nếu bạn chưa set `VITE_API_BASE_URL` trước khi deploy:

1. Vào **Vercel Dashboard** → Chọn project
2. Vào **Settings** → **Environment Variables**
3. Thêm hoặc cập nhật `VITE_API_BASE_URL`
4. Vào **Deployments** tab
5. Click **"..."** (3 chấm) trên deployment mới nhất
6. Chọn **"Redeploy"**
7. Đợi rebuild xong

---

## ✅ PHẦN 4: KIỂM TRA VÀ TEST

### Bước 4.1: Test Backend

1. Truy cập: `https://code-do-backend.onrender.com/docs`
2. Test một vài endpoints:
   - `GET /api/users/me` (cần đăng nhập)
   - `GET /api/courses` (public)
3. Kiểm tra response có đúng không

### Bước 4.2: Test Frontend

1. Truy cập: `https://code-do-frontend.vercel.app`
2. Test các chức năng:
   - Đăng ký tài khoản mới
   - Đăng nhập
   - Xem danh sách khóa học
   - Đăng ký khóa học
3. Mở Developer Tools (F12):
   - **Console tab**: Kiểm tra có lỗi JavaScript không
   - **Network tab**: Kiểm tra API calls có thành công không

### Bước 4.3: Kiểm tra CORS

Nếu gặp lỗi CORS:

1. Kiểm tra browser console (F12) → xem lỗi cụ thể
2. Kiểm tra `ALLOWED_ORIGINS` trên Render:
   - Phải là JSON array format: `["https://..."]`
   - URL phải khớp chính xác (không có trailing slash)
3. Kiểm tra `VITE_API_BASE_URL` trên Vercel:
   - Phải có `https://`
   - Không có trailing slash

---

## 🐛 TROUBLESHOOTING

### ❌ Backend không start được

**Lỗi:** `ModuleNotFoundError: No module named 'xxx'`

**Giải pháp:**
1. Kiểm tra `fastapi_app/requirements.txt` có đầy đủ packages không
2. Kiểm tra Build Command: `pip install -r fastapi_app/requirements.txt`
3. Xem Logs trên Render để biết package nào thiếu

**Lỗi:** `Database connection failed`

**Giải pháp:**
1. Kiểm tra `DATABASE_URL` trên Render:
   - Phải dùng **Internal Database URL**
   - Format: `postgresql+psycopg://user:pass@dpg-xxxxx-a/database`
2. Kiểm tra database đã được tạo chưa
3. Kiểm tra migrations đã chạy chưa

**Lỗi:** `Port already in use` hoặc `Address already in use`

**Giải pháp:**
- Không cần lo, Render tự động set `$PORT`
- Kiểm tra Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### ❌ Frontend không kết nối được Backend

**Lỗi:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Giải pháp:**
1. Kiểm tra `ALLOWED_ORIGINS` trên Render:
   - Phải có URL frontend: `["https://code-do-frontend.vercel.app"]`
   - Format phải là JSON array
2. Đảm bảo đã redeploy backend sau khi cập nhật
3. Clear browser cache và thử lại

**Lỗi:** `404 Not Found` khi gọi API

**Giải pháp:**
1. Kiểm tra `VITE_API_BASE_URL` trên Vercel:
   - Phải là URL backend: `https://code-do-backend.onrender.com`
   - Không có trailing slash
2. Kiểm tra API endpoint có đúng không
3. Kiểm tra Network tab trong browser để xem request URL

**Lỗi:** `Network Error` hoặc `Failed to fetch`

**Giải pháp:**
1. Kiểm tra backend có đang chạy không: Truy cập `/docs`
2. Kiểm tra `VITE_API_BASE_URL` có đúng không
3. Kiểm tra firewall hoặc network restrictions

### ❌ Build Failed

**Backend Build Failed:**
- Xem Logs trên Render → tìm lỗi cụ thể
- Kiểm tra `requirements.txt` có syntax error không
- Kiểm tra Python version (Render thường dùng Python 3.11)

**Frontend Build Failed:**
- Xem Logs trên Vercel → tìm lỗi cụ thể
- Kiểm tra `package.json` có đúng không
- Kiểm tra Node.js version (Vercel tự động detect)

---

## 📝 CHECKLIST DEPLOY

### Backend (Render)
- [ ] Đã tạo PostgreSQL database trên Render
- [ ] Đã chạy migrations trên database
- [ ] Đã tạo Web Service trên Render
- [ ] Đã kết nối GitHub repository
- [ ] Đã cấu hình đúng Build Command và Start Command
- [ ] Đã set đầy đủ Environment Variables:
  - [ ] `DATABASE_URL` (Internal URL với `+psycopg`)
  - [ ] `JWT_SECRET`
  - [ ] `JWT_ALG`
  - [ ] `ACCESS_TOKEN_EXPIRE_MINUTES`
  - [ ] `REFRESH_TOKEN_EXPIRE_MINUTES`
  - [ ] `ALLOWED_ORIGINS` (tạm thời localhost)
- [ ] Backend đã deploy thành công
- [ ] Có thể truy cập `/docs` endpoint
- [ ] Đã lưu URL backend

### Frontend (Vercel)
- [ ] Đã import repository vào Vercel
- [ ] Đã cấu hình đúng Root Directory (`frontend`)
- [ ] Đã set `VITE_API_BASE_URL` environment variable
- [ ] Frontend đã deploy thành công
- [ ] Đã lưu URL frontend

### Kết nối
- [ ] Đã cập nhật `ALLOWED_ORIGINS` trên Render với URL frontend
- [ ] Backend đã redeploy sau khi cập nhật CORS
- [ ] Frontend có thể kết nối với backend (không có lỗi CORS)

### Testing
- [ ] Backend API hoạt động (test qua `/docs`)
- [ ] Frontend có thể load được
- [ ] Đăng ký/đăng nhập hoạt động
- [ ] Các chức năng chính hoạt động bình thường
- [ ] Không có lỗi trong browser console

---

## 🔐 Lưu ý Bảo mật

1. **JWT_SECRET**: 
   - Phải là chuỗi ngẫu nhiên dài (ít nhất 32 ký tự)
   - Không được share với ai
   - Không được commit vào git

2. **DATABASE_URL**: 
   - Không được commit vào git
   - Chỉ dùng Internal URL trên Render
   - External URL chỉ dùng khi cần kết nối từ local

3. **ALLOWED_ORIGINS**: 
   - Chỉ cho phép domain frontend của bạn
   - Không thêm `*` hoặc wildcard

4. **Environment Variables**: 
   - Không share screenshots có chứa secrets
   - Sử dụng Render/Vercel secrets management

---

## 📞 Cần giúp đỡ?

Nếu gặp lỗi:

1. **Kiểm tra Logs:**
   - Render: Web Service → **Logs** tab
   - Vercel: Project → **Deployments** → Click deployment → **Logs**

2. **Kiểm tra Browser Console:**
   - Mở Developer Tools (F12)
   - Xem **Console** và **Network** tabs

3. **Kiểm tra Environment Variables:**
   - Render: Web Service → **Environment** tab
   - Vercel: Project → **Settings** → **Environment Variables**

4. **Kiểm tra Database:**
   - Render: Database → **Connect** tab
   - Test connection với psql

---

## 🎉 Hoàn thành!

Sau khi hoàn thành tất cả các bước:

- ✅ Backend đang chạy trên: `https://code-do-backend.onrender.com`
- ✅ Frontend đang chạy trên: `https://code-do-frontend.vercel.app`
- ✅ Database đang chạy trên Render
- ✅ Tất cả đã kết nối và hoạt động!

**Chúc mừng! Dự án của bạn đã được deploy thành công! 🚀**

---

## 📚 Tài liệu tham khảo

- Render Documentation: https://render.com/docs
- Vercel Documentation: https://vercel.com/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- Vite Documentation: https://vitejs.dev

