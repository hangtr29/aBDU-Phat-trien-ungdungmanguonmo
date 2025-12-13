from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional
from datetime import datetime

from ...db.session import get_db
from ...models.message import Message
from ...models.user import User, UserRole
from ...schemas.message import MessageCreate, MessageOut, ConversationOut
from ...api.deps import get_current_active_user

router = APIRouter()


def _can_message(current_user: User, target_user: User) -> bool:
    """Kiểm tra xem current_user có thể nhắn tin cho target_user không"""
    # Admin có thể nhắn tin với tất cả
    if current_user.role == UserRole.admin:
        return True
    
    # Giáo viên có thể nhắn tin với admin và học sinh
    if current_user.role == UserRole.teacher:
        return target_user.role in [UserRole.admin, UserRole.student]
    
    # Học sinh chỉ có thể nhắn tin với giáo viên
    if current_user.role == UserRole.student:
        return target_user.role == UserRole.teacher
    
    return False


@router.get("/messages/conversations", response_model=List[ConversationOut])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách các cuộc trò chuyện của user hiện tại"""
    # Lấy tất cả tin nhắn liên quan đến current_user
    all_messages = db.query(Message).filter(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).all()
    
    # Tạo set các user_id đã từng nhắn tin
    other_user_ids = set()
    for msg in all_messages:
        if msg.sender_id == current_user.id:
            other_user_ids.add(msg.receiver_id)
        else:
            other_user_ids.add(msg.sender_id)
    
    # Lấy thông tin user và tin nhắn cuối cùng
    conversations = []
    for other_user_id in other_user_ids:
        # Lấy thông tin user
        other_user = db.query(User).filter(User.id == other_user_id).first()
        if not other_user:
            continue
        
        # Kiểm tra quyền nhắn tin
        if not _can_message(current_user, other_user) and not _can_message(other_user, current_user):
            continue
        
        # Lấy tin nhắn cuối cùng
        last_message = db.query(Message).filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.receiver_id == current_user.id)
            )
        ).order_by(Message.created_at.desc()).first()
        
        # Đếm số tin nhắn chưa đọc
        unread_count = db.query(func.count(Message.id)).filter(
            Message.sender_id == other_user_id,
            Message.receiver_id == current_user.id,
            Message.da_doc == False
        ).scalar() or 0
        
        conversations.append(ConversationOut(
            user_id=other_user.id,
            user_name=other_user.ho_ten or "Unknown",
            user_email=other_user.email,
            user_role=other_user.role.value if other_user.role else None,
            last_message=last_message.noi_dung if last_message else None,
            last_message_time=last_message.created_at if last_message else None,
            unread_count=unread_count
        ))
    
    # Sắp xếp theo thời gian tin nhắn cuối cùng
    conversations.sort(key=lambda x: x.last_message_time or datetime.min, reverse=True)
    
    return conversations


@router.get("/messages/conversations/{other_user_id}", response_model=List[MessageOut])
def get_messages(
    other_user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách tin nhắn giữa current_user và other_user"""
    other_user = db.query(User).filter(User.id == other_user_id).first()
    if not other_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")
    
    # Kiểm tra quyền nhắn tin
    if not _can_message(current_user, other_user) and not _can_message(other_user, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền nhắn tin với người dùng này"
        )
    
    # Lấy tin nhắn
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == other_user_id),
            and_(Message.sender_id == other_user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
    
    # Đánh dấu tin nhắn đã đọc
    db.query(Message).filter(
        Message.sender_id == other_user_id,
        Message.receiver_id == current_user.id,
        Message.da_doc == False
    ).update({"da_doc": True})
    db.commit()
    
    # Thêm thông tin user vào response
    result = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.sender_id).first()
        receiver = db.query(User).filter(User.id == msg.receiver_id).first()
        
        result.append(MessageOut(
            id=msg.id,
            sender_id=msg.sender_id,
            receiver_id=msg.receiver_id,
            noi_dung=msg.noi_dung,
            da_doc=msg.da_doc,
            created_at=msg.created_at,
            sender_name=sender.ho_ten if sender else "Unknown",
            receiver_name=receiver.ho_ten if receiver else "Unknown",
            sender_role=sender.role.value if sender and sender.role else None,
            receiver_role=receiver.role.value if receiver and receiver.role else None
        ))
    
    return result


@router.post("/messages", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
def send_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Gửi tin nhắn"""
    receiver = db.query(User).filter(User.id == payload.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người nhận không tồn tại")
    
    if current_user.id == payload.receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể gửi tin nhắn cho chính mình")
    
    # Kiểm tra quyền nhắn tin
    if not _can_message(current_user, receiver):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền nhắn tin với người dùng này"
        )
    
    # Tạo tin nhắn
    message = Message(
        sender_id=current_user.id,
        receiver_id=payload.receiver_id,
        noi_dung=payload.noi_dung.strip()
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Trả về với thông tin user
    return MessageOut(
        id=message.id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        noi_dung=message.noi_dung,
        da_doc=message.da_doc,
        created_at=message.created_at,
        sender_name=current_user.ho_ten or "Unknown",
        receiver_name=receiver.ho_ten or "Unknown",
        sender_role=current_user.role.value if current_user.role else None,
        receiver_role=receiver.role.value if receiver.role else None
    )


@router.get("/messages/unread-count", response_model=dict)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy số tin nhắn chưa đọc"""
    count = db.query(func.count(Message.id)).filter(
        Message.receiver_id == current_user.id,
        Message.da_doc == False
    ).scalar() or 0
    
    return {"unread_count": count}


@router.get("/messages/available-users", response_model=List[ConversationOut])
def get_available_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách user có thể nhắn tin (chưa có conversation)"""
    # Lấy tất cả user đã từng nhắn tin
    existing_conversations = db.query(Message).filter(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).all()
    
    existing_user_ids = {current_user.id}
    for msg in existing_conversations:
        if msg.sender_id == current_user.id:
            existing_user_ids.add(msg.receiver_id)
        else:
            existing_user_ids.add(msg.sender_id)
    
    # Lấy tất cả user có thể nhắn tin
    all_users = db.query(User).filter(
        User.id != current_user.id,
        User.is_active == True
    ).all()
    
    available_users = []
    for user in all_users:
        if user.id in existing_user_ids:
            continue  # Đã có conversation rồi
        
        # Kiểm tra quyền nhắn tin
        if not _can_message(current_user, user) and not _can_message(user, current_user):
            continue
        
        available_users.append(ConversationOut(
            user_id=user.id,
            user_name=user.ho_ten or "Unknown",
            user_email=user.email,
            user_role=user.role.value if user.role else None,
            last_message=None,
            last_message_time=None,
            unread_count=0
        ))
    
    return available_users









