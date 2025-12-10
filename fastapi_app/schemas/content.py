from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContentBase(BaseModel):
    tieu_de_muc: str
    noi_dung: Optional[str] = None
    hinh_anh: Optional[str] = None
    video_path: Optional[str] = None
    video_duration: Optional[int] = 0
    thu_tu: Optional[int] = 0
    is_unlocked: Optional[bool] = True
    unlock_date: Optional[datetime] = None


class ContentCreate(ContentBase):
    pass


class ContentOut(ContentBase):
    id: int
    khoa_hoc_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

