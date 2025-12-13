# 💳 Hướng dẫn Payment Integration

## 📋 Tổng quan

Hệ thống đã có cơ sở hạ tầng cho payment integration, nhưng **chưa tích hợp với cổng thanh toán thật**. Hiện tại đang dùng **demo mode** để test.

## ✅ Đã có sẵn

### Backend
- ✅ Model `Payment` với đầy đủ trạng thái và phương thức thanh toán
- ✅ API endpoints:
  - `POST /api/payments/create` - Tạo đơn hàng và payment link
  - `POST /api/payments/callback` - Xử lý callback từ cổng thanh toán
  - `GET /api/payments/me` - Lấy danh sách thanh toán của user
  - `POST /api/payments/demo-complete` - Demo: Tự động hoàn thành thanh toán
  - `GET /api/payments/{payment_id}` - Chi tiết một payment

### Frontend
- ✅ Component `PaymentModal` để hiển thị form thanh toán
- ✅ Tích hợp vào trang chi tiết khóa học

### Database
- ✅ Bảng `thanh_toan` với đầy đủ các trường cần thiết

## 🔧 Các phương thức thanh toán hỗ trợ

```python
class PaymentMethod(str, enum.Enum):
    momo = "momo"           # Ví MoMo
    zalopay = "zalopay"     # Ví ZaloPay
    paypal = "paypal"       # PayPal
    bank_transfer = "bank_transfer"  # Chuyển khoản ngân hàng
```

## 📝 Trạng thái thanh toán

```python
class PaymentStatus(str, enum.Enum):
    pending = "pending"      # Chờ thanh toán
    processing = "processing"  # Đang xử lý
    completed = "completed"  # Đã thanh toán thành công
    failed = "failed"       # Thanh toán thất bại
    cancelled = "cancelled"  # Đã hủy
```

## 🚀 Cách tích hợp với cổng thanh toán thật

### Bước 1: Chọn cổng thanh toán

**Các lựa chọn phổ biến tại Việt Nam:**
- **MoMo** - https://developers.momo.vn/
- **ZaloPay** - https://developers.zalopay.vn/
- **VNPay** - https://sandbox.vnpayment.vn/
- **PayPal** - https://developer.paypal.com/

### Bước 2: Cài đặt SDK/Thư viện

Ví dụ với MoMo:
```bash
pip install momo-python-sdk
```

Hoặc dùng HTTP requests trực tiếp.

### Bước 3: Cập nhật file `.env`

Thêm các biến môi trường:
```env
# MoMo
MOMO_PARTNER_CODE=your_partner_code
MOMO_ACCESS_KEY=your_access_key
MOMO_SECRET_KEY=your_secret_key
MOMO_ENVIRONMENT=sandbox  # hoặc production

# ZaloPay
ZALOPAY_APP_ID=your_app_id
ZALOPAY_KEY1=your_key1
ZALOPAY_KEY2=your_key2
```

### Bước 4: Tạo service xử lý thanh toán

Tạo file `fastapi_app/services/payment_service.py`:

```python
from typing import Optional
from decimal import Decimal
from ..models.payment import Payment, PaymentMethod
from ..core.config import settings

class PaymentService:
    @staticmethod
    def create_momo_payment(payment: Payment) -> str:
        """Tạo payment link với MoMo"""
        # TODO: Tích hợp với MoMo API
        # Xem: https://developers.momo.vn/#/docs/en/ai/online/home
        
        partner_code = settings.momo_partner_code
        access_key = settings.momo_access_key
        secret_key = settings.momo_secret_key
        
        # Tạo request data
        request_data = {
            "partnerCode": partner_code,
            "partnerName": "E-Learning Platform",
            "storeId": "E-Learning",
            "requestId": payment.ma_don_hang,
            "amount": int(payment.so_tien * 100),  # Convert to cents
            "orderId": payment.ma_don_hang,
            "orderInfo": f"Thanh toan khoa hoc #{payment.khoa_hoc_id}",
            "redirectUrl": f"{settings.frontend_url}/payment/callback",
            "ipnUrl": f"{settings.backend_url}/api/payments/callback",
            "lang": "vi",
            "extraData": ""
        }
        
        # Tạo signature và gọi API
        # ... (xem documentation của MoMo)
        
        return payment_url
    
    @staticmethod
    def verify_callback(data: dict, method: PaymentMethod) -> bool:
        """Xác thực callback từ cổng thanh toán"""
        if method == PaymentMethod.momo:
            # Verify MoMo signature
            # ...
            return True
        elif method == PaymentMethod.zalopay:
            # Verify ZaloPay signature
            # ...
            return True
        return False
```

### Bước 5: Cập nhật API route

Sửa file `fastapi_app/api/routes/payments.py`:

```python
from ...services.payment_service import PaymentService

@router.post("/create", response_model=PaymentLinkResponse)
def create_payment(...):
    # ... existing code ...
    
    # Thay vì tạo URL giả lập:
    # payment_url = f"/payment/process/{payment.id}?method={payload.phuong_thuc.value}"
    
    # Tạo URL thật từ cổng thanh toán:
    if payload.phuong_thuc == PaymentMethod.momo:
        payment_url = PaymentService.create_momo_payment(payment)
    elif payload.phuong_thuc == PaymentMethod.zalopay:
        payment_url = PaymentService.create_zalopay_payment(payment)
    # ...
    
    return PaymentLinkResponse(...)
```

### Bước 6: Cập nhật callback handler

```python
@router.post("/callback")
def payment_callback(payload: dict, db: Session = Depends(get_db)):
    """Xử lý callback từ cổng thanh toán"""
    
    # Xác thực callback
    method = PaymentMethod(payload.get("method", "momo"))
    if not PaymentService.verify_callback(payload, method):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Tìm payment
    ma_don_hang = payload.get("orderId") or payload.get("ma_don_hang")
    payment = db.query(Payment).filter(
        Payment.ma_don_hang == ma_don_hang
    ).first()
    
    # Cập nhật trạng thái
    if payload.get("resultCode") == 0:  # MoMo success code
        payment.trang_thai = PaymentStatus.completed
        payment.ma_giao_dich = payload.get("transId")
        # ... tự động đăng ký khóa học
    else:
        payment.trang_thai = PaymentStatus.failed
    
    db.commit()
    return payment
```

## 🧪 Testing với Demo Mode

Hiện tại có endpoint demo để test:

```javascript
// Frontend: PaymentModal.jsx
// Đang dùng endpoint demo:
POST /api/payments/demo-complete
{
  "ma_don_hang": "ORDER_..."
}
```

## 📚 Tài liệu tham khảo

### MoMo
- Documentation: https://developers.momo.vn/
- Sandbox: https://test-payment.momo.vn/
- Python SDK: https://github.com/momo-wallet/payment-sdk-python

### ZaloPay
- Documentation: https://developers.zalopay.vn/
- Sandbox: https://sandbox.zalopay.vn/

### VNPay
- Documentation: https://sandbox.vnpayment.vn/apis/
- Integration guide: https://sandbox.vnpayment.vn/apis/docs/checkout/

### PayPal
- Documentation: https://developer.paypal.com/docs/
- Sandbox: https://developer.paypal.com/dashboard/

## ⚠️ Lưu ý bảo mật

1. **Không commit keys vào git**: Dùng `.env` và `.gitignore`
2. **Xác thực callback**: Luôn verify signature từ cổng thanh toán
3. **HTTPS**: Chỉ dùng HTTPS trong production
4. **Validate amount**: Kiểm tra số tiền từ callback khớp với database
5. **Idempotency**: Xử lý callback nhiều lần (idempotent)

## 🔄 Workflow thanh toán

```
1. User chọn khóa học có phí
2. Click "Đăng ký" → Hiện PaymentModal
3. Chọn phương thức thanh toán
4. Frontend gọi POST /api/payments/create
5. Backend tạo Payment record (status: pending)
6. Backend tạo payment URL từ cổng thanh toán
7. Frontend redirect user đến cổng thanh toán
8. User thanh toán trên cổng thanh toán
9. Cổng thanh toán gọi callback: POST /api/payments/callback
10. Backend xác thực và cập nhật Payment (status: completed)
11. Backend tự động tạo Enrollment
12. Cổng thanh toán redirect về frontend với kết quả
13. Frontend hiển thị kết quả và cập nhật UI
```

## 📝 TODO

- [ ] Tích hợp MoMo API
- [ ] Tích hợp ZaloPay API
- [ ] Tích hợp VNPay API
- [ ] Tích hợp PayPal API
- [ ] Thêm webhook handler cho các cổng thanh toán
- [ ] Thêm email notification khi thanh toán thành công
- [ ] Thêm admin dashboard để xem thống kê thanh toán
- [ ] Thêm refund functionality

---

**Cập nhật**: 2024-12-12

