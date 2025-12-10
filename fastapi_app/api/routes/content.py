from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
from datetime import datetime

from ...db.session import get_db
from ...models.course_content import CourseContent
from ...models.course import Course
from ...schemas.content import ContentCreate, ContentOut
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()

# Tạo thư mục uploads nếu chưa có
UPLOAD_DIR = "static/uploads/videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/courses/{course_id}/lessons", response_model=list[ContentOut])
def list_lessons(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    return db.query(CourseContent).filter(CourseContent.khoa_hoc_id == course_id).order_by(CourseContent.thu_tu).all()


@router.post("/courses/{course_id}/lessons", response_model=ContentOut, status_code=status.HTTP_201_CREATED)
def create_lesson(
    course_id: int,
    tieu_de_muc: str = Form(...),
    noi_dung: Optional[str] = Form(None),
    thu_tu: int = Form(0),
    is_unlocked: bool = Form(True),
    unlock_date: Optional[str] = Form(None),
    video_path: Optional[str] = Form(None),
    video_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Kiểm tra khóa học tồn tại
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    # Xử lý file upload nếu có
    final_video_path = video_path
    if video_file:
        # Lưu file video
        file_ext = os.path.splitext(video_file.filename)[1]
        filename = f"{course_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            content = video_file.file.read()
            buffer.write(content)
        
        final_video_path = f"/static/uploads/videos/{filename}"
    
    # Parse unlock_date nếu có
    unlock_dt = None
    if unlock_date:
        try:
            unlock_dt = datetime.fromisoformat(unlock_date.replace('Z', '+00:00'))
        except:
            pass
    
    lesson = CourseContent(
        khoa_hoc_id=course_id,
        tieu_de_muc=tieu_de_muc,
        noi_dung=noi_dung,
        thu_tu=thu_tu,
        is_unlocked=is_unlocked,
        unlock_date=unlock_dt,
        video_path=final_video_path
    )
    
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

