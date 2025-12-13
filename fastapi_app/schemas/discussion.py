from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DiscussionBase(BaseModel):
    noi_dung: str


class DiscussionCreate(DiscussionBase):
    parent_id: Optional[int] = None  # ID của thảo luận cha (nếu là reply)


class DiscussionOut(DiscussionBase):
    id: int
    khoa_hoc_id: int
    user_id: int
    parent_id: Optional[int] = None
    hinh_anh: Optional[str] = None
    created_at: Optional[datetime] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    replies: Optional[List['DiscussionOut']] = []  # Danh sách replies

    class Config:
        from_attributes = True


# Forward reference resolution
DiscussionOut.model_rebuild()

