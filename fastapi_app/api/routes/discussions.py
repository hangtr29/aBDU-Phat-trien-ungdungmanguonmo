from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid

from ...db.session import get_db
from ...models.discussion import Discussion
from ...models.course import Course
from ...schemas.discussion import DiscussionCreate, DiscussionOut
from ...api.deps import get_current_active_user
from ...models.user import User, UserRole

router = APIRouter()
MAX_CONTENT_LEN = 2000
DISCUSSION_IMAGES_DIR = "static/uploads/discussions"
os.makedirs(DISCUSSION_IMAGES_DIR, exist_ok=True)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]


def _ensure_course(db: Session, course_id: int) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    return course


@router.get("/courses/{course_id}/discussions", response_model=list[DiscussionOut])
def list_discussions(
    course_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    _ensure_course(db, course_id)
    # Lấy chỉ các thảo luận gốc (không có parent_id)
    discussions = (
        db.query(Discussion)
        .filter(
            Discussion.khoa_hoc_id == course_id,
            Discussion.parent_id.is_(None)  # Chỉ lấy thảo luận gốc
        )
        .order_by(Discussion.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Thêm thông tin user và replies cho mỗi discussion
    result = []
    for discussion in discussions:
        user = db.query(User).filter(User.id == discussion.user_id).first()
        
        # Lấy tất cả replies của thảo luận này
        replies = db.query(Discussion).filter(
            Discussion.parent_id == discussion.id
        ).order_by(Discussion.created_at.asc()).all()
        
        replies_out = []
        for reply in replies:
            reply_user = db.query(User).filter(User.id == reply.user_id).first()
            replies_out.append(DiscussionOut(
                id=reply.id,
                khoa_hoc_id=reply.khoa_hoc_id,
                user_id=reply.user_id,
                parent_id=reply.parent_id,
                noi_dung=reply.noi_dung,
                hinh_anh=reply.hinh_anh,
                created_at=reply.created_at,
                user_name=reply_user.ho_ten if reply_user else "Unknown",
                user_email=reply_user.email if reply_user else None,
                user_role=reply_user.role.value if reply_user and reply_user.role else None,
                replies=[]
            ))
        
        # Tạo DiscussionOut với thông tin user và replies
        discussion_out = DiscussionOut(
            id=discussion.id,
            khoa_hoc_id=discussion.khoa_hoc_id,
            user_id=discussion.user_id,
            parent_id=discussion.parent_id,
            noi_dung=discussion.noi_dung,
            hinh_anh=discussion.hinh_anh,
            created_at=discussion.created_at,
            user_name=user.ho_ten if user else "Unknown",
            user_email=user.email if user else None,
            user_role=user.role.value if user and user.role else None,
            replies=replies_out
        )
        result.append(discussion_out)
    
    return result


@router.post("/courses/{course_id}/discussions", response_model=DiscussionOut, status_code=status.HTTP_201_CREATED)
async def create_discussion(
    course_id: int,
    noi_dung: str = Form(...),
    parent_id: Optional[int] = Form(None),
    hinh_anh: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    _ensure_course(db, course_id)
    content = (noi_dung or "").strip()
    if not content and not hinh_anh:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nội dung hoặc hình ảnh không được để trống")
    if len(content) > MAX_CONTENT_LEN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nội dung quá dài (tối đa 2000 ký tự)")

    # Xử lý upload hình ảnh nếu có
    image_path = None
    if hinh_anh and hinh_anh.filename:
        # Kiểm tra loại file
        if hinh_anh.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Loại file không được hỗ trợ. Chỉ chấp nhận: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )
        
        # Đọc file
        contents = await hinh_anh.read()
        
        # Kiểm tra kích thước
        if len(contents) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Hình ảnh quá lớn. Kích thước tối đa: {MAX_IMAGE_SIZE / 1024 / 1024}MB"
            )
        
        # Tạo tên file unique
        file_ext = os.path.splitext(hinh_anh.filename)[1] or '.jpg'
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path_save = os.path.join(DISCUSSION_IMAGES_DIR, unique_filename)
        
        # Lưu file
        with open(file_path_save, "wb") as f:
            f.write(contents)
        
        # Đường dẫn để trả về cho client
        image_path = f"/static/uploads/discussions/{unique_filename}"

    # Nếu là reply, kiểm tra parent discussion tồn tại
    if parent_id:
        parent_discussion = db.query(Discussion).filter(
            Discussion.id == parent_id,
            Discussion.khoa_hoc_id == course_id
        ).first()
        if not parent_discussion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thảo luận cha không tồn tại"
            )

    discussion = Discussion(
        khoa_hoc_id=course_id,
        user_id=current_user.id,
        noi_dung=content if content else "",
        parent_id=parent_id,
        hinh_anh=image_path
    )

    db.add(discussion)
    db.commit()
    db.refresh(discussion)
    
    # Tạo thông báo
    try:
        from ...api.routes.notifications import create_notification_for_discussion
        course = _ensure_course(db, course_id)
        
        # Nếu là reply, thông báo cho người tạo thảo luận gốc
        if parent_id:
            parent_discussion = db.query(Discussion).filter(Discussion.id == parent_id).first()
            if parent_discussion and parent_discussion.user_id != current_user.id:
                parent_user = db.query(User).filter(User.id == parent_discussion.user_id).first()
                if parent_user:
                    from ...models.notification import Notification
                    notification = Notification(
                        user_id=parent_user.id,
                        loai="discussion_reply",
                        tieu_de=f"💬 Có người trả lời thảo luận của bạn",
                        noi_dung=f"{current_user.ho_ten} đã trả lời thảo luận của bạn trong khóa học '{course.tieu_de if course else ''}'",
                        link=f"/learn/{course_id}?tab=discussion"
                    )
                    db.add(notification)
                    db.commit()
        # Nếu là thảo luận mới, thông báo cho giáo viên
        elif course and course.teacher_id and current_user.id != course.teacher_id:
            create_notification_for_discussion(
                db, discussion.id, course_id, current_user.id, course.teacher_id
            )
    except Exception as e:
        print(f"Failed to create notification: {e}")
    
    # Trả về discussion với thông tin user
    user = db.query(User).filter(User.id == discussion.user_id).first()
    return DiscussionOut(
        id=discussion.id,
        khoa_hoc_id=discussion.khoa_hoc_id,
        user_id=discussion.user_id,
        parent_id=discussion.parent_id,
        noi_dung=discussion.noi_dung,
        hinh_anh=discussion.hinh_anh,
        created_at=discussion.created_at,
        user_name=user.ho_ten if user else "Unknown",
        user_email=user.email if user else None,
        user_role=user.role.value if user and user.role else None,
        replies=[]
    )


@router.delete("/discussions/{discussion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thảo luận không tồn tại")

    # Chủ sở hữu hoặc admin/teacher được xóa
    if discussion.user_id != current_user.id and current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền xóa nội dung này")

    db.delete(discussion)
    db.commit()
    return None


