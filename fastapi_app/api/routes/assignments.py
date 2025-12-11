from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid

from ...db.session import get_db
from ...models.assignment import Assignment, Submission
from ...models.course import Course
from ...schemas.assignment import AssignmentCreate, AssignmentOut, SubmissionCreate, SubmissionOut
from ...api.deps import get_current_active_user
from ...models.user import User, UserRole

router = APIRouter()

UPLOAD_DIR = "static/uploads/assignments"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _ensure_course(db: Session, course_id: int) -> Course:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    return course


def _ensure_assignment(db: Session, assignment_id: int) -> Assignment:
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bài tập không tồn tại")
    return assignment


@router.get("/courses/{course_id}/assignments", response_model=list[AssignmentOut])
def list_assignments(course_id: int, db: Session = Depends(get_db)):
    try:
        _ensure_course(db, course_id)
        assignments = (
            db.query(Assignment)
            .filter(Assignment.khoa_hoc_id == course_id)
            .order_by(Assignment.han_nop.nulls_last())
            .all()
        )
        # Convert Decimal to float để serialize đúng
        result = []
        for a in assignments:
            result.append(AssignmentOut(
                id=a.id,
                khoa_hoc_id=a.khoa_hoc_id,
                tieu_de=a.tieu_de,
                noi_dung=a.noi_dung,
                han_nop=a.han_nop,
                is_required=a.is_required,
                diem_toi_da=float(a.diem_toi_da) if a.diem_toi_da else 10.0,
                created_at=a.created_at
            ))
        return result
    except Exception as e:
        import traceback
        print(f"Error in list_assignments: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Lỗi khi lấy danh sách bài tập: {str(e)}")


@router.post("/courses/{course_id}/assignments", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def create_assignment(
    course_id: int,
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # Kiểm tra quyền giáo viên hoặc admin
        if current_user.role not in [UserRole.teacher, UserRole.admin]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ giáo viên mới có thể tạo bài tập")
        
        _ensure_course(db, course_id)
        
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
        
        # Tạo thông báo cho tất cả học viên đã đăng ký khóa học
        try:
            from ...models.enrollment import Enrollment
            enrollments = db.query(Enrollment).filter(
                Enrollment.khoa_hoc_id == course_id,
                Enrollment.trang_thai == 'active'
            ).all()
            
            from ...models.notification import Notification
            for enrollment in enrollments:
                notification = Notification(
                    user_id=enrollment.user_id,
                    loai="assignment",
                    tieu_de=f"Bài tập mới: {payload.tieu_de}",
                    noi_dung=f"Giáo viên đã tạo bài tập mới cho khóa học",
                    link=f"/learn/{course_id}?tab=assignments"
                )
                db.add(notification)
            db.commit()
        except Exception as e:
            # Không làm gián đoạn flow nếu notification fail
            print(f"Failed to create notifications: {e}")
        
        return assignment
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        db.rollback()
        print(f"Error in create_assignment: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Lỗi khi tạo bài tập: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        db.rollback()
        print(f"Error in create_assignment: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Lỗi khi tạo bài tập: {str(e)}")


@router.post("/assignments/{assignment_id}/submit", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
def submit_assignment(
    assignment_id: int,
    noi_dung: Optional[str] = None,
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assignment = _ensure_assignment(db, assignment_id)

    if not noi_dung and not file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cần nhập nội dung hoặc đính kèm file")

    file_path = None
    if file:
        file_bytes = file.file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File vượt quá 10MB")
        ext = os.path.splitext(file.filename)[1]
        filename = f"{assignment_id}_{current_user.id}_{uuid.uuid4().hex}{ext}"
        disk_path = os.path.join(UPLOAD_DIR, filename)
        with open(disk_path, "wb") as buffer:
            buffer.write(file_bytes)
        file_path = f"/static/uploads/assignments/{filename}"

    # Cho phép nộp lại: update nếu đã tồn tại, ngược lại tạo mới
    submission = (
        db.query(Submission)
        .filter(Submission.bai_tap_id == assignment_id, Submission.user_id == current_user.id)
        .first()
    )
    if submission:
        submission.noi_dung = noi_dung
        submission.file_path = file_path or submission.file_path
        submission.trang_thai = "submitted"
    else:
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
    
    # Tạo thông báo cho giáo viên
    try:
        from ...api.routes.notifications import create_notification_for_submission
        assignment_obj = _ensure_assignment(db, assignment_id)
        if assignment_obj:
            from ...models.course import Course
            course = db.query(Course).filter(Course.id == assignment_obj.khoa_hoc_id).first()
            if course and course.teacher_id:
                create_notification_for_submission(
                    db, submission.id, assignment_id, current_user.id, course.teacher_id
                )
    except Exception as e:
        # Không làm gián đoạn flow nếu notification fail
        print(f"Failed to create notification: {e}")
    
    return submission


@router.get("/assignments/{assignment_id}/submissions")
def list_submissions(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bài tập không tồn tại")
    
    from ...models.user import User as UserModel
    
    # Chỉ giáo viên hoặc admin mới xem được tất cả submissions
    if current_user.role in [UserRole.teacher, UserRole.admin]:
        submissions = db.query(Submission).filter(Submission.bai_tap_id == assignment_id).all()
    else:
        # Học viên chỉ xem được submission của mình
        submissions = db.query(Submission).filter(
            Submission.bai_tap_id == assignment_id,
            Submission.user_id == current_user.id
        ).all()
    
    # Thêm thông tin user vào mỗi submission
    result = []
    for sub in submissions:
        user = db.query(UserModel).filter(UserModel.id == sub.user_id).first()
        sub_dict = {
            **sub.__dict__,
            "user": {
                "id": user.id if user else None,
                "ho_ten": user.ho_ten if user else None,
                "email": user.email if user else None
            } if user else None
        }
        result.append(sub_dict)
    
    return result


@router.post("/submissions/{submission_id}/grade", response_model=SubmissionOut)
def grade_submission(
    submission_id: int,
    diem: float,
    nhan_xet: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ giáo viên mới có thể chấm bài")
    
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bài nộp không tồn tại")

    assignment = _ensure_assignment(db, submission.bai_tap_id)
    if assignment.diem_toi_da is not None and diem > float(assignment.diem_toi_da):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Điểm vượt quá điểm tối đa của bài")
    
    submission.diem = diem
    submission.nhan_xet = nhan_xet
    submission.trang_thai = "graded"
    
    db.commit()
    db.refresh(submission)
    
    # Tạo thông báo cho học viên
    try:
        from ...api.routes.notifications import create_notification_for_grade
        create_notification_for_grade(
            db, submission.id, assignment.id, submission.user_id, float(diem)
        )
    except Exception as e:
        print(f"Failed to create notification: {e}")
    
    return submission



