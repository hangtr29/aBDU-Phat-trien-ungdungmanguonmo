from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from ...db.session import get_db
from ...models.progress import Progress
from ...models.course_content import CourseContent
from ...schemas.progress import ProgressCreate, ProgressOut
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.post("/courses/{course_id}/progress", response_model=ProgressOut, status_code=status.HTTP_201_CREATED)
def update_progress(
    course_id: int,
    lesson_id: Optional[int] = None,
    completed: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Tìm hoặc tạo progress record
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == course_id,
        Progress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        # Tính progress percentage
        total_lessons = db.query(CourseContent).filter(CourseContent.khoa_hoc_id == course_id).count()
        completed_lessons = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.course_id == course_id,
            Progress.completed == True
        ).count()
        
        if completed:
            completed_lessons += 1
        
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        progress = Progress(
            user_id=current_user.id,
            course_id=course_id,
            lesson_id=lesson_id,
            completed=completed,
            progress_percentage=progress_percentage
        )
        db.add(progress)
    else:
        progress.completed = completed
        # Recalculate percentage
        total_lessons = db.query(CourseContent).filter(CourseContent.khoa_hoc_id == course_id).count()
        completed_lessons = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.course_id == course_id,
            Progress.completed == True
        ).count()
        if completed and not progress.completed:
            completed_lessons += 1
        elif not completed and progress.completed:
            completed_lessons -= 1
        
        progress.progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    db.commit()
    db.refresh(progress)
    return progress


@router.get("/courses/{course_id}/progress", response_model=ProgressOut)
def get_progress(
    course_id: int,
    lesson_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    progress = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.course_id == course_id,
        Progress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        # Tính progress tổng thể cho course
        total_lessons = db.query(CourseContent).filter(CourseContent.khoa_hoc_id == course_id).count()
        completed_lessons = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.course_id == course_id,
            Progress.completed == True
        ).count()
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        return {
            "id": 0,
            "user_id": current_user.id,
            "course_id": course_id,
            "lesson_id": lesson_id,
            "completed": False,
            "progress_percentage": progress_percentage,
            "updated_at": None
        }
    
    return progress


@router.get("/users/me/progress")
def get_all_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy tất cả progress của user"""
    progress_list = db.query(Progress).filter(Progress.user_id == current_user.id).all()
    return progress_list

