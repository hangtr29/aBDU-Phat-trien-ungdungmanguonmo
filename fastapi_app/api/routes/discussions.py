from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models.discussion import Discussion
from ...models.course import Course
from ...schemas.discussion import DiscussionCreate, DiscussionOut
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.get("/courses/{course_id}/discussions", response_model=list[DiscussionOut])
def list_discussions(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    return db.query(Discussion).filter(Discussion.khoa_hoc_id == course_id).order_by(Discussion.created_at.desc()).all()


@router.post("/courses/{course_id}/discussions", response_model=DiscussionOut, status_code=status.HTTP_201_CREATED)
def create_discussion(
    course_id: int,
    payload: DiscussionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    discussion = Discussion(
        khoa_hoc_id=course_id,
        user_id=current_user.id,
        noi_dung=payload.noi_dung
    )
    
    db.add(discussion)
    db.commit()
    db.refresh(discussion)
    return discussion

