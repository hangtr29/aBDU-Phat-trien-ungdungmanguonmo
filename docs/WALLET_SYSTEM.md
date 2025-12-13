# 💰 Hệ thống Ví và Nạp tiền

## 📋 Tổng quan

Hệ thống đã được cập nhật để sử dụng **ví nội bộ** thay vì tích hợp trực tiếp với cổng thanh toán. Người dùng sẽ nạp tiền vào ví, sau đó dùng số dư trong ví để thanh toán khóa học.

## ✅ Đã triển khai

### Backend
- ✅ Thêm cột `so_du` vào bảng `users` (số dư ví)
- ✅ API `/api/wallet/balance` - Lấy số dư ví
- ✅ API `/api/wallet/add-funds` - Tạo yêu cầu nạp tiền và QR code
- ✅ API `/api/wallet/verify-payment` - Xác thực thanh toán (admin)

### Frontend
- ✅ Hiển thị số dư ví trên header (màu xanh lá)
- ✅ Trang `/addfunds` với layout 3 cột:
  - **Bên trái**: Thông tin người nhận (STK, Tên, Nội dung chuyển khoản)
  - **Ở giữa**: QR Code VietQR
  - **Bên phải**: Nhập số tiền, nút Tạo QR, Reset

### Database
- ✅ Migration: `database/add_user_balance.sql`

## 🚀 Cách sử dụng

### 1. Chạy Migration

```powershell
# Chạy migration để thêm cột so_du
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U elearn -d elearning -f database\add_user_balance.sql
```

Hoặc dùng Python:
```python
python -c "from fastapi_app.db.session import SessionLocal; from sqlalchemy import text; db = SessionLocal(); db.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS so_du NUMERIC(12, 2) DEFAULT 0 NOT NULL')); db.commit()"
```

### 2. Cấu hình thông tin ngân hàng

Sửa file `fastapi_app/api/routes/wallet.py`:

```python
BANK_ACCOUNT = {
    "stk": "1234567890",  # Số tài khoản thật
    "ten_nguoi_nhan": "CONG TY E-LEARNING",  # Tên người nhận
    "ten_ngan_hang": "Vietcombank"  # Tên ngân hàng
}
```

Hoặc tốt hơn, thêm vào `.env`:
```env
BANK_STK=1234567890
BANK_TEN_NGUOI_NHAN=CONG TY E-LEARNING
BANK_TEN_NGAN_HANG=Vietcombank
```

### 3. Workflow nạp tiền

1. User click vào "Số dư X VND" trên header
2. Chuyển đến trang `/addfunds`
3. Nhập số tiền (tối thiểu 50,000 VNĐ, chỉ số nguyên)
4. Nhấn "Tạo QR"
5. Hệ thống tạo:
   - Nội dung chuyển khoản: `NAPTIEN_{user_id}_{random_string}`
   - QR Code VietQR với đầy đủ thông tin
6. User quét QR code bằng app ngân hàng
7. User copy nội dung chuyển khoản và paste khi chuyển tiền
8. Sau khi chuyển khoản, admin xác nhận qua API `/api/wallet/verify-payment`
9. Số dư được cập nhật tự động

## 📝 API Endpoints

### GET `/api/wallet/balance`
Lấy thông tin số dư ví

**Response:**
```json
{
  "so_du": 100000.00,
  "stk": "1234567890",
  "ten_nguoi_nhan": "CONG TY E-LEARNING"
}
```

### POST `/api/wallet/add-funds`
Tạo yêu cầu nạp tiền

**Request:**
```json
{
  "so_tien": 100000
}
```

**Response:**
```json
{
  "stk": "1234567890",
  "ten_nguoi_nhan": "CONG TY E-LEARNING",
  "ten_ngan_hang": "Vietcombank",
  "noi_dung_chuyen_khoan": "NAPTIEN_1_ABC123XY",
  "so_tien": 100000,
  "qr_code_data": "https://vietqr.net/soan-ma-qr?..."
}
```

### POST `/api/wallet/verify-payment`
Xác thực thanh toán (admin hoặc user tự xác thực)

**Request:**
```json
{
  "noi_dung": "NAPTIEN_1_ABC123XY",
  "so_tien": 100000
}
```

## 🔧 Cập nhật Payment System

Cần cập nhật logic thanh toán khóa học để trừ từ ví thay vì gọi cổng thanh toán:

```python
# fastapi_app/api/routes/enrollments.py hoặc payments.py

@router.post("/courses/{course_id}/enroll")
def enroll_course(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if course.gia and course.gia > 0:
        # Kiểm tra số dư
        if (current_user.so_du or 0) < course.gia:
            raise HTTPException(
                status_code=402,
                detail="Số dư không đủ. Vui lòng nạp thêm tiền."
            )
        
        # Trừ tiền từ ví
        current_user.so_du = (current_user.so_du or 0) - course.gia
        db.commit()
    
    # Tạo enrollment
    enrollment = Enrollment(...)
    db.add(enrollment)
    db.commit()
    
    return enrollment
```

## 🎨 UI Components

### Hiển thị số dư
- Màu xanh lá (#28a745)
- Format: "Số dư X,XXX,XXX VND"
- Click vào sẽ chuyển đến `/addfunds`

### Trang AddFunds
- Layout responsive 3 cột
- QR Code tự động tạo khi nhập số tiền
- Copy button cho mỗi thông tin
- Validation: tối thiểu 50,000 VNĐ, chỉ số nguyên

## ⚠️ Lưu ý

1. **Nội dung chuyển khoản**: Phải unique để xác định user
2. **Xác thực thanh toán**: Cần có cơ chế admin xác nhận hoặc tự động (nếu có webhook từ ngân hàng)
3. **Bảo mật**: Không để lộ thông tin tài khoản ngân hàng trong code
4. **VietQR**: Format URL có thể thay đổi, cần kiểm tra documentation

## 🔄 Cải tiến tương lai

- [ ] Tích hợp webhook từ ngân hàng để tự động xác nhận
- [ ] Thêm lịch sử giao dịch nạp tiền
- [ ] Thêm admin dashboard để xác nhận thanh toán
- [ ] Thêm email/SMS notification khi nạp tiền thành công
- [ ] Hỗ trợ nhiều tài khoản ngân hàng

---

**Cập nhật**: 2024-12-12

