from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import datetime


class WalletInfoResponse(BaseModel):
    """Thông tin số dư ví"""
    so_du: Decimal
    stk: str
    ten_nguoi_nhan: str


class AddFundsRequest(BaseModel):
    """Request nạp tiền"""
    so_tien: Decimal = Field(..., ge=50000, description="Số tiền nạp (tối thiểu 50,000 VNĐ)")


class AddFundsResponse(BaseModel):
    """Response khi tạo yêu cầu nạp tiền"""
    stk: str
    ten_nguoi_nhan: str
    ten_ngan_hang: str
    noi_dung_chuyen_khoan: str
    so_tien: Decimal
    qr_code_data: str  # URL hoặc data để tạo QR code


class QRCodeData(BaseModel):
    """Dữ liệu QR code"""
    qr_data: str
    amount: Decimal
    content: str

class SubmitPaymentRequest(BaseModel):
    """Request xác nhận đã thanh toán"""
    noi_dung_chuyen_khoan: str
    so_tien: Decimal  # Số tiền đã chuyển khoản


class DepositTransactionOut(BaseModel):
    """Thông tin giao dịch nạp tiền"""
    id: int
    user_id: int
    so_tien: Decimal
    ma_giao_dich: str
    noi_dung_chuyen_khoan: str
    trang_thai: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_name: Optional[str] = None

    class Config:
        from_attributes = True

