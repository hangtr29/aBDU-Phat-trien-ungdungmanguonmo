from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EnrollmentBase(BaseModel):
    khoa_hoc_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentOut(EnrollmentBase):
    id: int
    user_id: int
    trang_thai: str
    ngay_dang_ky: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

