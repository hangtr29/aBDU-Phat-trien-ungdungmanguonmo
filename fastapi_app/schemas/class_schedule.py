from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClassScheduleBase(BaseModel):
    tieu_de: str
    mo_ta: Optional[str] = None
    ngay_hoc: datetime
    thoi_gian_bat_dau: Optional[str] = None  # Format: "HH:MM"
    thoi_gian_ket_thuc: Optional[str] = None  # Format: "HH:MM"
    link_google_meet: Optional[str] = None
    link_zoom: Optional[str] = None
    link_khac: Optional[str] = None
    ghi_chu: Optional[str] = None


class ClassScheduleCreate(ClassScheduleBase):
    khoa_hoc_id: int


class ClassScheduleUpdate(BaseModel):
    tieu_de: Optional[str] = None
    mo_ta: Optional[str] = None
    ngay_hoc: Optional[datetime] = None
    thoi_gian_bat_dau: Optional[str] = None
    thoi_gian_ket_thuc: Optional[str] = None
    link_google_meet: Optional[str] = None
    link_zoom: Optional[str] = None
    link_khac: Optional[str] = None
    ghi_chu: Optional[str] = None
    is_completed: Optional[bool] = None


class ClassScheduleOut(ClassScheduleBase):
    id: int
    khoa_hoc_id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    khoa_hoc: Optional[dict] = None  # Thông tin khóa học (nếu có)

    class Config:
        from_attributes = True

