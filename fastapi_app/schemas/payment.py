from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from ..models.payment import PaymentStatus, PaymentMethod


class PaymentBase(BaseModel):
    khoa_hoc_id: int
    phuong_thuc: PaymentMethod
    so_tien: Decimal


class PaymentCreate(PaymentBase):
    pass


class PaymentOut(PaymentBase):
    id: int
    user_id: int
    trang_thai: PaymentStatus
    ma_giao_dich: Optional[str] = None
    ma_don_hang: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    ngay_thanh_toan: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaymentCallback(BaseModel):
    """Schema cho callback từ cổng thanh toán"""
    ma_giao_dich: str
    ma_don_hang: str
    trang_thai: str  # success, failed, cancelled
    so_tien: Optional[Decimal] = None
    thong_tin_them: Optional[str] = None


class PaymentLinkResponse(BaseModel):
    """Response khi tạo payment link"""
    payment_url: str
    ma_don_hang: str
    expires_at: Optional[datetime] = None

