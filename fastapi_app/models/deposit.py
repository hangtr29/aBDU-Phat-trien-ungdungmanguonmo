import enum
from sqlalchemy import Column, Integer, Numeric, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base


class DepositStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class DepositTransaction(Base):
    __tablename__ = "deposit_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    so_tien = Column(Numeric(12, 2), nullable=False)
    ma_giao_dich = Column(String(50), unique=True, nullable=False, index=True)
    noi_dung_chuyen_khoan = Column(String(255), nullable=False)
    trang_thai = Column(Enum(DepositStatus), default=DepositStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", backref="deposit_transactions")

