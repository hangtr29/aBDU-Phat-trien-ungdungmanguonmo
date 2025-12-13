from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List

from ...db.session import get_db
from ...models.assignment import Assignment
from ...models.enrollment import Enrollment
from ...models.notification import Notification
from ...models.user import User

router = APIRouter()


def check_and_notify_upcoming_deadlines(db: Session):
    """
    Kiểm tra bài tập sắp hết hạn (trong vòng 24h) và gửi thông báo cho học viên chưa nộp bài
    """
    now = datetime.utcnow()
    # Bài tập sắp hết hạn trong vòng 24 giờ
    deadline_threshold = now + timedelta(hours=24)
    
    # Lấy tất cả bài tập có hạn nộp trong vòng 24h
    upcoming_assignments = db.query(Assignment).filter(
        and_(
            Assignment.han_nop.isnot(None),
            Assignment.han_nop > now,
            Assignment.han_nop <= deadline_threshold
        )
    ).all()
    
    notifications_created = 0
    
    for assignment in upcoming_assignments:
        # Lấy tất cả học viên đã đăng ký khóa học
        enrollments = db.query(Enrollment).filter(
            Enrollment.khoa_hoc_id == assignment.khoa_hoc_id,
            Enrollment.trang_thai == 'active'
        ).all()
        
        for enrollment in enrollments:
            # Kiểm tra học viên đã nộp bài chưa
            from ...models.assignment import Submission
            submission = db.query(Submission).filter(
                Submission.bai_tap_id == assignment.id,
                Submission.user_id == enrollment.user_id,
                Submission.trang_thai != 'cancelled'
            ).first()
            
            # Nếu chưa nộp bài, kiểm tra xem đã có thông báo chưa
            if not submission:
                # Kiểm tra xem đã có thông báo về deadline này trong 12h qua chưa (tránh spam)
                recent_notification = db.query(Notification).filter(
                    Notification.user_id == enrollment.user_id,
                    Notification.loai == 'assignment_deadline',
                    Notification.link.like(f'%assignments%{assignment.id}%'),
                    Notification.created_at >= now - timedelta(hours=12)
                ).first()
                
                if not recent_notification:
                    # Tính thời gian còn lại
                    time_left = assignment.han_nop - now
                    hours_left = int(time_left.total_seconds() / 3600)
                    minutes_left = int((time_left.total_seconds() % 3600) / 60)
                    
                    # Format thông báo
                    if hours_left > 0:
                        time_str = f"{hours_left} giờ"
                        if minutes_left > 0:
                            time_str += f" {minutes_left} phút"
                    else:
                        time_str = f"{minutes_left} phút"
                    
                    notification = Notification(
                        user_id=enrollment.user_id,
                        loai="assignment_deadline",
                        tieu_de=f"⚠️ Bài tập sắp hết hạn: {assignment.tieu_de}",
                        noi_dung=f"Bài tập '{assignment.tieu_de}' sẽ hết hạn trong {time_str}. Vui lòng nộp bài sớm!",
                        link=f"/learn/{assignment.khoa_hoc_id}?tab=assignments"
                    )
                    db.add(notification)
                    notifications_created += 1
    
    if notifications_created > 0:
        db.commit()
    
    return notifications_created


@router.post("/check-deadlines")
def check_deadlines(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Endpoint để kiểm tra và gửi thông báo bài tập sắp hết hạn
    Có thể gọi định kỳ hoặc khi user login
    """
    background_tasks.add_task(check_and_notify_upcoming_deadlines, db)
    return {"message": "Đang kiểm tra bài tập sắp hết hạn..."}


@router.get("/check-deadlines-sync")
def check_deadlines_sync(db: Session = Depends(get_db)):
    """
    Kiểm tra và gửi thông báo đồng bộ (trả về số lượng thông báo đã tạo)
    """
    count = check_and_notify_upcoming_deadlines(db)
    return {"notifications_created": count, "message": f"Đã tạo {count} thông báo"}









