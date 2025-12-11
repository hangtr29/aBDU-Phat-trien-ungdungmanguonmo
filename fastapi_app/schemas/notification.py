from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    loai: str
    tieu_de: str
    noi_dung: Optional[str] = None
    link: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: int


class NotificationOut(NotificationBase):
    id: int
    user_id: int
    da_doc: bool
    created_at: datetime

    class Config:
        from_attributes = True

