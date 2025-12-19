from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, distinct
from typing import List

from ...db.session import get_db
from ...api.deps import get_current_active_user
from ...models.user import User, UserRole
from ...models.course import Course
from ...models.enrollment import Enrollment
from ...models.assignment import Assignment, Submission
from ...models import progress as progress_model

router = APIRouter()


@router.get("/teachers/me/students")
def get_teacher_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách học viên đã mua khóa học của giáo viên kèm phần trăm hoàn thành"""
    if current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên mới có quyền"
        )
    
    # Lấy tất cả khóa học của giáo viên
    courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()
    course_ids = [course.id for course in courses]
    
    if not course_ids:
        return []
    
    # Lấy tất cả học viên đã đăng ký các khóa học này
    enrollments = db.query(Enrollment).filter(
        Enrollment.khoa_hoc_id.in_(course_ids),
        Enrollment.trang_thai == 'active'
    ).all()
    
    result = []
    for enrollment in enrollments:
        # Enrollment có thể dùng student_id hoặc user_id tùy model
        student_id = getattr(enrollment, 'student_id', None) or getattr(enrollment, 'user_id', None)
        if not student_id:
            continue
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            continue
        
        course = db.query(Course).filter(Course.id == enrollment.khoa_hoc_id).first()
        if not course:
            continue
        
        # Tính phần trăm hoàn thành
        # Lấy tổng số bài học
        from ...models.course_content import Lesson
        total_lessons = db.query(func.count(Lesson.id)).filter(
            Lesson.khoa_hoc_id == enrollment.khoa_hoc_id
        ).scalar() or 0
        
        # Lấy số bài học đã hoàn thành
        from ...models.progress import Progress
        completed_lessons = db.query(func.count(Progress.id)).filter(
            Progress.user_id == student_id,
            Progress.khoa_hoc_id == enrollment.khoa_hoc_id,
            Progress.completed == True
        ).scalar() or 0
        
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        result.append({
            "student_id": student.id,
            "student_name": student.ho_ten,
            "student_email": student.email,
            "course_id": course.id,
            "course_name": course.tieu_de,
            "progress_percentage": round(progress_percentage, 1),
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "enrolled_at": enrollment.created_at if hasattr(enrollment, 'created_at') else None
        })
    
    return result


@router.get("/teachers/me/pending-submissions")
def get_pending_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách bài tập cần chấm (chưa được chấm)"""
    if current_user.role not in [UserRole.teacher, UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên mới có quyền"
        )
    
    # Lấy tất cả khóa học của giáo viên
    courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()
    course_ids = [course.id for course in courses]
    
    if not course_ids:
        return []
    
    # Lấy tất cả bài tập của các khóa học này
    assignments = db.query(Assignment).filter(
        Assignment.khoa_hoc_id.in_(course_ids)
    ).all()
    assignment_ids = [a.id for a in assignments]
    
    if not assignment_ids:
        return []
    
    # Lấy tất cả submissions của các bài tập này (để debug)
    all_submissions = db.query(Submission).filter(
        Submission.bai_tap_id.in_(assignment_ids)
    ).all()
    print(f"[DEBUG] Teacher {current_user.id}: Total submissions: {len(all_submissions)}")
    for sub in all_submissions:
        print(f"[DEBUG] Submission {sub.id}: bai_tap_id={sub.bai_tap_id}, diem={sub.diem}, trang_thai={sub.trang_thai}, user_id={sub.user_id}")
    
    # Lấy tất cả submissions chưa được chấm (diem is None)
    # Đơn giản: chỉ cần kiểm tra diem is None, vì khi chấm bài sẽ set diem và đổi trang_thai thành 'graded'
    pending_submissions = db.query(Submission).filter(
        Submission.bai_tap_id.in_(assignment_ids),
        Submission.diem.is_(None)
    ).order_by(Submission.ngay_nop.desc()).all()
    
    print(f"[DEBUG] Teacher {current_user.id}: Found {len(pending_submissions)} pending submissions")
    
    result = []
    for submission in pending_submissions:
        assignment = db.query(Assignment).filter(Assignment.id == submission.bai_tap_id).first()
        if not assignment:
            continue
        
        course = db.query(Course).filter(Course.id == assignment.khoa_hoc_id).first()
        if not course:
            continue
        
        student = db.query(User).filter(User.id == submission.user_id).first()
        if not student:
            continue
        
        result.append({
            "submission_id": submission.id,
            "assignment_id": assignment.id,
            "assignment_title": assignment.tieu_de,
            "course_id": course.id,
            "course_name": course.tieu_de,
            "student_id": student.id,
            "student_name": student.ho_ten,
            "student_email": student.email,
            "submission_content": submission.noi_dung,
            "file_path": submission.file_path,
            "submitted_at": submission.ngay_nop,
            "max_score": float(assignment.diem_toi_da) if assignment.diem_toi_da else 10.0
        })
    
    return result









