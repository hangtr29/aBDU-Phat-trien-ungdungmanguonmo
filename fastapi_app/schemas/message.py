from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    noi_dung: str


class MessageCreate(MessageBase):
    receiver_id: int


class MessageOut(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    da_doc: bool
    created_at: datetime
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None
    sender_role: Optional[str] = None
    receiver_role: Optional[str] = None

    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    user_id: int
    user_name: str
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int = 0

    class Config:
        from_attributes = True

