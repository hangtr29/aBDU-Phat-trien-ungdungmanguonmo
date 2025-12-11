from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models.notification import Notification
from ...models.user import User
from ...schemas.notification import NotificationOut, NotificationCreate
from ...api.deps import get_current_active_user

router = APIRouter()


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách thông báo của user hiện tại"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.da_doc == False)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
    return notifications


@router.get("/notifications/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Đếm số thông báo chưa đọc"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.da_doc == False
    ).count()
    return {"count": count}


@router.put("/notifications/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Đánh dấu thông báo đã đọc"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thông báo không tồn tại")
    
    notification.da_doc = True
    db.commit()
    return {"message": "Đã đánh dấu đã đọc"}


@router.put("/notifications/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Đánh dấu tất cả thông báo đã đọc"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.da_doc == False
    ).update({"da_doc": True})
    db.commit()
    return {"message": "Đã đánh dấu tất cả đã đọc"}


@router.post("/notifications", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Tạo thông báo mới (admin hoặc hệ thống)"""
    # Chỉ admin mới có thể tạo thông báo cho người khác
    if payload.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền tạo thông báo")
    
    notification = Notification(
        user_id=payload.user_id,
        loai=payload.loai,
        tieu_de=payload.tieu_de,
        noi_dung=payload.noi_dung,
        link=payload.link
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


# Helper function để tạo thông báo tự động
def create_notification_for_submission(
    db: Session,
    submission_id: int,
    assignment_id: int,
    student_id: int,
    teacher_id: int
):
    """Tạo thông báo cho giáo viên khi học viên nộp bài"""
    from ...models.assignment import Assignment
    from ...models.user import User
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    student = db.query(User).filter(User.id == student_id).first()
    
    if assignment and student:
        notification = Notification(
            user_id=teacher_id,
            loai="submission",
            tieu_de=f"Học viên {student.ho_ten} đã nộp bài tập",
            noi_dung=f"Bài tập: {assignment.tieu_de}",
            link=f"/grade/{assignment.khoa_hoc_id}/{assignment_id}"
        )
        db.add(notification)
        db.commit()


def create_notification_for_discussion(
    db: Session,
    discussion_id: int,
    course_id: int,
    student_id: int,
    teacher_id: int
):
    """Tạo thông báo cho giáo viên khi học viên đặt câu hỏi"""
    from ...models.user import User
    
    student = db.query(User).filter(User.id == student_id).first()
    
    if student:
        notification = Notification(
            user_id=teacher_id,
            loai="discussion",
            tieu_de=f"Học viên {student.ho_ten} đã đặt câu hỏi",
            noi_dung="Có câu hỏi mới trong khóa học của bạn",
            link=f"/learn/{course_id}?tab=discussion"
        )
        db.add(notification)
        db.commit()


def create_notification_for_grade(
    db: Session,
    submission_id: int,
    assignment_id: int,
    student_id: int,
    diem: float
):
    """Tạo thông báo cho học viên khi được chấm điểm"""
    from ...models.assignment import Assignment
    
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    if assignment:
        notification = Notification(
            user_id=student_id,
            loai="grade",
            tieu_de=f"Bài tập đã được chấm điểm",
            noi_dung=f"Bài tập '{assignment.tieu_de}' đã được chấm: {diem}/{assignment.diem_toi_da} điểm",
            link=f"/learn/{assignment.khoa_hoc_id}?tab=assignments"
        )
        db.add(notification)
        db.commit()

