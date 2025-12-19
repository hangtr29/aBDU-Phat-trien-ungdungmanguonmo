from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...db.session import get_db
from ...models.class_schedule import ClassSchedule
from ...models.course import Course
from ...models.enrollment import Enrollment
from ...schemas.class_schedule import ClassScheduleCreate, ClassScheduleUpdate, ClassScheduleOut
from ...api.deps import get_current_active_user
from ...models.user import User, UserRole

router = APIRouter()


@router.get("/courses/{course_id}/schedule", response_model=List[ClassScheduleOut])
def get_course_schedule(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy thời khóa biểu của khóa học - Học sinh đã đăng ký hoặc giáo viên của khóa học"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    # Kiểm tra quyền: học sinh phải đã đăng ký, giáo viên phải là owner, admin có quyền xem tất cả
    if current_user.role == UserRole.student:
        enrollment = db.query(Enrollment).filter(
            Enrollment.khoa_hoc_id == course_id,
            Enrollment.user_id == current_user.id
        ).first()
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn chưa đăng ký khóa học này"
            )
    elif current_user.role == UserRole.teacher:
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không phải giáo viên của khóa học này"
            )
    elif current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền truy cập"
        )
    
    schedules = db.query(ClassSchedule).filter(
        ClassSchedule.khoa_hoc_id == course_id
    ).order_by(ClassSchedule.ngay_hoc.asc()).all()
    
    # Thêm thông tin khóa học vào response
    result = []
    for schedule in schedules:
        schedule_dict = {
            "id": schedule.id,
            "khoa_hoc_id": schedule.khoa_hoc_id,
            "tieu_de": schedule.tieu_de,
            "mo_ta": schedule.mo_ta,
            "ngay_hoc": schedule.ngay_hoc,
            "thoi_gian_bat_dau": schedule.thoi_gian_bat_dau,
            "thoi_gian_ket_thuc": schedule.thoi_gian_ket_thuc,
            "link_google_meet": schedule.link_google_meet,
            "link_zoom": schedule.link_zoom,
            "link_khac": schedule.link_khac,
            "ghi_chu": schedule.ghi_chu,
            "is_completed": schedule.is_completed,
            "created_at": schedule.created_at,
            "updated_at": schedule.updated_at,
            "khoa_hoc": {
                "id": course.id,
                "tieu_de": course.tieu_de
            } if course else None
        }
        result.append(schedule_dict)
    
    return result


@router.post("/courses/{course_id}/schedule", response_model=ClassScheduleOut, status_code=status.HTTP_201_CREATED)
def create_schedule(
    course_id: int,
    payload: ClassScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Tạo lịch học mới - Chỉ giáo viên của khóa học hoặc admin"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    # Kiểm tra quyền
    if current_user.role == UserRole.teacher:
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ giáo viên của khóa học mới có quyền tạo lịch học"
            )
    elif current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên hoặc admin mới có quyền"
        )
    
    # Đảm bảo course_id trong payload khớp với URL
    if payload.khoa_hoc_id != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course_id trong payload không khớp với URL"
        )
    
    schedule = ClassSchedule(
        khoa_hoc_id=payload.khoa_hoc_id,
        tieu_de=payload.tieu_de,
        mo_ta=payload.mo_ta,
        ngay_hoc=payload.ngay_hoc,
        thoi_gian_bat_dau=payload.thoi_gian_bat_dau,
        thoi_gian_ket_thuc=payload.thoi_gian_ket_thuc,
        link_google_meet=payload.link_google_meet,
        link_zoom=payload.link_zoom,
        link_khac=payload.link_khac,
        ghi_chu=payload.ghi_chu
    )
    
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.put("/schedule/{schedule_id}", response_model=ClassScheduleOut)
def update_schedule(
    schedule_id: int,
    payload: ClassScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cập nhật lịch học - Chỉ giáo viên của khóa học hoặc admin"""
    schedule = db.query(ClassSchedule).filter(ClassSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lịch học không tồn tại")
    
    course = db.query(Course).filter(Course.id == schedule.khoa_hoc_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    # Kiểm tra quyền
    if current_user.role == UserRole.teacher:
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ giáo viên của khóa học mới có quyền chỉnh sửa lịch học"
            )
    elif current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên hoặc admin mới có quyền"
        )
    
    # Cập nhật các trường
    if payload.tieu_de is not None:
        schedule.tieu_de = payload.tieu_de
    if payload.mo_ta is not None:
        schedule.mo_ta = payload.mo_ta
    if payload.ngay_hoc is not None:
        schedule.ngay_hoc = payload.ngay_hoc
    if payload.thoi_gian_bat_dau is not None:
        schedule.thoi_gian_bat_dau = payload.thoi_gian_bat_dau
    if payload.thoi_gian_ket_thuc is not None:
        schedule.thoi_gian_ket_thuc = payload.thoi_gian_ket_thuc
    if payload.link_google_meet is not None:
        schedule.link_google_meet = payload.link_google_meet
    if payload.link_zoom is not None:
        schedule.link_zoom = payload.link_zoom
    if payload.link_khac is not None:
        schedule.link_khac = payload.link_khac
    if payload.ghi_chu is not None:
        schedule.ghi_chu = payload.ghi_chu
    if payload.is_completed is not None:
        schedule.is_completed = payload.is_completed
    
    db.commit()
    db.refresh(schedule)
    return schedule


@router.delete("/schedule/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Xóa lịch học - Chỉ giáo viên của khóa học hoặc admin"""
    schedule = db.query(ClassSchedule).filter(ClassSchedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lịch học không tồn tại")
    
    course = db.query(Course).filter(Course.id == schedule.khoa_hoc_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    
    # Kiểm tra quyền
    if current_user.role == UserRole.teacher:
        if course.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ giáo viên của khóa học mới có quyền xóa lịch học"
            )
    elif current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ giáo viên hoặc admin mới có quyền"
        )
    
    db.delete(schedule)
    db.commit()
    return {"message": "Đã xóa lịch học thành công"}


@router.get("/students/my-schedule", response_model=List[ClassScheduleOut])
def get_my_schedule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy thời khóa biểu của tất cả khóa học đã đăng ký - Dành cho học sinh"""
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ học sinh mới có quyền truy cập"
        )
    
    # Lấy tất cả enrollment của học sinh
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == current_user.id).all()
    course_ids = [e.khoa_hoc_id for e in enrollments]
    
    if not course_ids:
        return []
    
    # Lấy tất cả lịch học của các khóa học đã đăng ký
    schedules = db.query(ClassSchedule).filter(
        ClassSchedule.khoa_hoc_id.in_(course_ids)
    ).order_by(ClassSchedule.ngay_hoc.asc()).all()
    
    # Thêm thông tin khóa học vào response
    result = []
    for schedule in schedules:
        course = db.query(Course).filter(Course.id == schedule.khoa_hoc_id).first()
        schedule_dict = {
            "id": schedule.id,
            "khoa_hoc_id": schedule.khoa_hoc_id,
            "tieu_de": schedule.tieu_de,
            "mo_ta": schedule.mo_ta,
            "ngay_hoc": schedule.ngay_hoc,
            "thoi_gian_bat_dau": schedule.thoi_gian_bat_dau,
            "thoi_gian_ket_thuc": schedule.thoi_gian_ket_thuc,
            "link_google_meet": schedule.link_google_meet,
            "link_zoom": schedule.link_zoom,
            "link_khac": schedule.link_khac,
            "ghi_chu": schedule.ghi_chu,
            "is_completed": schedule.is_completed,
            "created_at": schedule.created_at,
            "updated_at": schedule.updated_at,
            "khoa_hoc": {
                "id": course.id,
                "tieu_de": course.tieu_de
            } if course else None
        }
        result.append(schedule_dict)
    
    return result

