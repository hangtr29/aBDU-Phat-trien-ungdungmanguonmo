import enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class PaymentStatus(str, enum.Enum):
    pending = "pending"  # Chờ thanh toán
    processing = "processing"  # Đang xử lý
    completed = "completed"  # Đã thanh toán thành công
    failed = "failed"  # Thanh toán thất bại
    cancelled = "cancelled"  # Đã hủy


class PaymentMethod(str, enum.Enum):
    momo = "momo"
    zalopay = "zalopay"
    paypal = "paypal"
    bank_transfer = "bank_transfer"  # Chuyển khoản ngân hàng


class Payment(Base):
    __tablename__ = "thanh_toan"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    khoa_hoc_id = Column(Integer, ForeignKey("khoa_hoc.id"), nullable=False)
    so_tien = Column(Numeric(10, 2), nullable=False)
    phuong_thuc = Column(Enum(PaymentMethod), nullable=False)
    trang_thai = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    
    # Thông tin giao dịch từ cổng thanh toán
    ma_giao_dich = Column(String(100), unique=True, index=True)  # Transaction ID từ cổng thanh toán
    ma_don_hang = Column(String(100), unique=True, index=True)  # Order ID của hệ thống
    thong_tin_them = Column(Text)  # JSON string chứa thông tin thêm từ cổng thanh toán
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    ngay_thanh_toan = Column(DateTime(timezone=True))  # Thời điểm thanh toán thành công

    user = relationship("User", backref="payments")
    course = relationship("Course", backref="payments")

