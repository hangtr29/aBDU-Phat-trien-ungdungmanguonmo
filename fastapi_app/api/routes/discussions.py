from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models.discussion import Discussion
from ...models.course import Course
from ...schemas.discussion import DiscussionCreate, DiscussionOut
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()
MAX_CONTENT_LEN = 2000


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
    return (
        db.query(Discussion)
        .filter(Discussion.khoa_hoc_id == course_id)
        .order_by(Discussion.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/courses/{course_id}/discussions", response_model=DiscussionOut, status_code=status.HTTP_201_CREATED)
def create_discussion(
    course_id: int,
    payload: DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    _ensure_course(db, course_id)
    content = (payload.noi_dung or "").strip()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nội dung không được để trống")
    if len(content) > MAX_CONTENT_LEN:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nội dung quá dài (tối đa 2000 ký tự)")

    discussion = Discussion(
        khoa_hoc_id=course_id,
        user_id=current_user.id,
        noi_dung=content
    )

    db.add(discussion)
    db.commit()
    db.refresh(discussion)
    
    # Tạo thông báo cho giáo viên nếu học viên đặt câu hỏi
    try:
        from ...api.routes.notifications import create_notification_for_discussion
        course = _ensure_course(db, course_id)
        if course and course.teacher_id and current_user.id != course.teacher_id:
            create_notification_for_discussion(
                db, discussion.id, course_id, current_user.id, course.teacher_id
            )
    except Exception as e:
        print(f"Failed to create notification: {e}")
    
    return discussion


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


