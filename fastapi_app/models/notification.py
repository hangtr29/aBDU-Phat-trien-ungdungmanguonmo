from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..db.base import Base


class Notification(Base):
    __tablename__ = "thong_bao"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loai = Column(String(50), nullable=False)  # submission, discussion, grade, course, etc.
    tieu_de = Column(String(200), nullable=False)
    noi_dung = Column(Text)
    link = Column(String(500))  # Link đến trang liên quan
    da_doc = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", backref="notifications")

