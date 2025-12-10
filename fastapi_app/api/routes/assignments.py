from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os

from ...db.session import get_db
from ...models.assignment import Assignment, Submission
from ...models.course import Course
from ...schemas.assignment import AssignmentCreate, AssignmentOut, SubmissionCreate, SubmissionOut
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()

UPLOAD_DIR = "static/uploads/assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/courses/{course_id}/assignments", response_model=list[AssignmentOut])
def list_assignments(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    return db.query(Assignment).filter(Assignment.khoa_hoc_id == course_id).all()


@router.post("/courses/{course_id}/assignments", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(
    course_id: int,
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Kiểm tra quyền giáo viên hoặc admin
    if current_user.vai_tro not in ['teacher', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ giáo viên mới có thể tạo bài tập")
    
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    assignment = Assignment(
        khoa_hoc_id=course_id,
        tieu_de=payload.tieu_de,
        noi_dung=payload.noi_dung,
        han_nop=payload.han_nop,
        is_required=payload.is_required,
        diem_toi_da=payload.diem_toi_da
    )
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.post("/assignments/{assignment_id}/submit", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
def submit_assignment(
    assignment_id: int,
    noi_dung: Optional[str] = None,
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bài tập không tồn tại")
    
    file_path = None
    if file:
        filename = f"{assignment_id}_{current_user.id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        file_path = f"/static/uploads/assignments/{filename}"
    
    submission = Submission(
        bai_tap_id=assignment_id,
        user_id=current_user.id,
        noi_dung=noi_dung,
        file_path=file_path,
        trang_thai="submitted"
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/assignments/{assignment_id}/submissions", response_model=list[SubmissionOut])
def list_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bài tập không tồn tại")
    
    # Chỉ giáo viên hoặc admin mới xem được tất cả submissions
    if current_user.vai_tro in ['teacher', 'admin']:
        return db.query(Submission).filter(Submission.bai_tap_id == assignment_id).all()
    else:
        # Học viên chỉ xem được submission của mình
        return db.query(Submission).filter(
            Submission.bai_tap_id == assignment_id,
            Submission.user_id == current_user.id
        ).all()


@router.post("/submissions/{submission_id}/grade", response_model=SubmissionOut)
def grade_submission(
    submission_id: int,
    diem: float,
    nhan_xet: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.vai_tro not in ['teacher', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ giáo viên mới có thể chấm bài")
    
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bài nộp không tồn tại")
    
    submission.diem = diem
    submission.nhan_xet = nhan_xet
    submission.trang_thai = "graded"
    
    db.commit()
    db.refresh(submission)
    return submission

