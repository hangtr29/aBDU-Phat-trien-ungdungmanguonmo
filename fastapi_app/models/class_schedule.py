from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db.base import Base


class ClassSchedule(Base):
    """Thời khóa biểu học - Giáo viên tạo lịch học cho khóa học"""
    __tablename__ = "thoi_khoa_bieu"

    id = Column(Integer, primary_key=True, index=True)
    khoa_hoc_id = Column(Integer, ForeignKey("khoa_hoc.id"), nullable=False)
    tieu_de = Column(String(200), nullable=False)  # Ví dụ: "Buổi 1: Giới thiệu Python"
    mo_ta = Column(Text)  # Mô tả nội dung buổi học
    ngay_hoc = Column(DateTime(timezone=True), nullable=False)  # Ngày giờ học
    thoi_gian_bat_dau = Column(String(10))  # Ví dụ: "19:00"
    thoi_gian_ket_thuc = Column(String(10))  # Ví dụ: "21:00"
    link_google_meet = Column(String(500))  # Link Google Meet
    link_zoom = Column(String(500))  # Link Zoom (backup)
    link_khac = Column(String(500))  # Link khác nếu có
    ghi_chu = Column(Text)  # Ghi chú thêm cho học sinh
    is_completed = Column(Boolean, default=False)  # Đã học xong chưa
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    khoa_hoc = relationship("Course", backref="schedules")

