# 🔧 Sửa lỗi Frontend không kết nối được Backend

## Vấn đề

Frontend trên Vercel (`https://bdu-phat-trien-ungdungmanguonmo-delta.vercel.app`) chưa kết nối được với Backend trên Render (`https://code-do-backend.onrender.com`).

## Nguyên nhân

1. **VITE_API_BASE_URL** chưa được set trên Vercel
2. **ALLOWED_ORIGINS** trên Render chưa có URL frontend của Vercel
3. Backend có thể chưa chạy hoặc có lỗi

## Giải pháp

### Bước 1: Kiểm tra Backend có đang chạy không

1. Mở trình duyệt
2. Truy cập: `https://code-do-backend.onrender.com/docs`
3. Nếu thấy Swagger UI → Backend đang chạy ✅
4. Nếu không thấy hoặc lỗi → Backend có vấn đề, cần kiểm tra logs trên Render

### Bước 2: Cấu hình VITE_API_BASE_URL trên Vercel

1. **Vào Vercel Dashboard:**
   - Truy cập: https://vercel.com
   - Đăng nhập
   - Chọn project: `bdu-phat-trien-ungdungmanguonmo-delta`

2. **Vào Settings:**
   - Click tab **"Settings"** (ở trên cùng)
   - Click **"Environment Variables"** (sidebar bên trái)

3. **Thêm hoặc cập nhật biến:**
   - Tìm biến `VITE_API_BASE_URL`
   - Nếu chưa có: Click **"Add New"**
   - Nếu đã có: Click **"Edit"** (icon bút chì)
   
4. **Điền thông tin:**
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** `https://code-do-backend.onrender.com`
   - **Environment:** Chọn tất cả (Production, Preview, Development)
   - Click **"Save"**

5. **Redeploy:**
   - Vào tab **"Deployments"**
   - Tìm deployment mới nhất
   - Click **"..."** (3 chấm) → **"Redeploy"**
   - Chọn **"Use existing Build Cache"** hoặc **"Rebuild"**
   - Click **"Redeploy"**
   - Đợi 2-5 phút

### Bước 3: Cấu hình CORS trên Render

1. **Vào Render Dashboard:**
   - Truy cập: https://dashboard.render.com
   - Chọn Web Service: `code-do-backend`

2. **Vào Environment Variables:**
   - Click tab **"Environment"** (ở trên cùng)

3. **Tìm và cập nhật ALLOWED_ORIGINS:**
   - Tìm biến `ALLOWED_ORIGINS`
   - Click **"Edit"** (icon bút chì)
   - Thay đổi giá trị thành:
     ```
     ["https://bdu-phat-trien-ungdungmanguonmo-delta.vercel.app"]
     ```
   - **Lưu ý:** 
     - Phải là JSON array format
     - URL không có trailing slash `/`
     - Phải có `https://`
   - Click **"Save Changes"**

4. **Render sẽ tự động redeploy:**
   - Đợi 1-2 phút để redeploy xong

### Bước 4: Kiểm tra kết nối

1. **Mở Frontend:**
   - Truy cập: `https://bdu-phat-trien-ungdungmanguonmo-delta.vercel.app/courses`

2. **Mở Browser Console:**
   - Nhấn `F12` hoặc `Ctrl+Shift+I`
   - Click tab **"Console"**

3. **Kiểm tra lỗi:**
   - Nếu có lỗi CORS: Kiểm tra lại `ALLOWED_ORIGINS` trên Render
   - Nếu có lỗi 404: Kiểm tra `VITE_API_BASE_URL` trên Vercel
   - Nếu có lỗi Network: Kiểm tra backend có đang chạy không

4. **Kiểm tra Network tab:**
   - Click tab **"Network"**
   - Refresh trang
   - Tìm các request đến `/api/...`
   - Kiểm tra:
     - Status code (phải là 200, không phải 404 hoặc CORS error)
     - Request URL (phải là `https://code-do-backend.onrender.com/api/...`)

## Checklist

- [ ] Backend đang chạy (truy cập `/docs` thấy Swagger UI)
- [ ] `VITE_API_BASE_URL` đã được set trên Vercel = `https://code-do-backend.onrender.com`
- [ ] Frontend đã được redeploy sau khi set environment variable
- [ ] `ALLOWED_ORIGINS` trên Render đã có URL frontend
- [ ] Backend đã redeploy sau khi cập nhật CORS
- [ ] Không có lỗi trong browser console
- [ ] API calls thành công (status 200) trong Network tab

## Troubleshooting

### Lỗi: CORS policy: No 'Access-Control-Allow-Origin' header

**Nguyên nhân:** `ALLOWED_ORIGINS` trên Render chưa có URL frontend

**Giải pháp:**
1. Kiểm tra `ALLOWED_ORIGINS` trên Render
2. Đảm bảo URL frontend đúng format: `["https://bdu-phat-trien-ungdungmanguonmo-delta.vercel.app"]`
3. Redeploy backend

### Lỗi: 404 Not Found khi gọi API

**Nguyên nhân:** `VITE_API_BASE_URL` chưa được set hoặc sai

**Giải pháp:**
1. Kiểm tra `VITE_API_BASE_URL` trên Vercel
2. Đảm bảo giá trị: `https://code-do-backend.onrender.com` (không có trailing slash)
3. Redeploy frontend

### Lỗi: Network Error hoặc Failed to fetch

**Nguyên nhân:** Backend không chạy hoặc URL sai

**Giải pháp:**
1. Kiểm tra backend có chạy không: `https://code-do-backend.onrender.com/docs`
2. Kiểm tra `VITE_API_BASE_URL` có đúng không
3. Kiểm tra logs trên Render để xem backend có lỗi không

### Frontend vẫn không kết nối được sau khi đã cấu hình

**Giải pháp:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Thử incognito mode
3. Kiểm tra lại tất cả các bước trên
4. Xem logs trên Vercel và Render để tìm lỗi cụ thể

## Kiểm tra nhanh

Mở browser console và chạy:

```javascript
// Kiểm tra environment variable
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL);

// Test API call
fetch('https://code-do-backend.onrender.com/api/courses')
  .then(res => res.json())
  .then(data => console.log('API Response:', data))
  .catch(err => console.error('API Error:', err));
```

Nếu `VITE_API_BASE_URL` là `undefined` → Chưa set trên Vercel  
Nếu API call thành công → Kết nối OK  
Nếu API call lỗi CORS → Cần cập nhật `ALLOWED_ORIGINS` trên Render

