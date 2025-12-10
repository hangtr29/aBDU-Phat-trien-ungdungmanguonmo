from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models.course import Course
from ...schemas.course import CourseCreate, CourseOut

router = APIRouter()


@router.get("/courses", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khóa học không tồn tại")
    return course


@router.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    course = Course(
        tieu_de=payload.tieu_de,
        mo_ta=payload.mo_ta,
        cap_do=payload.cap_do,
        hinh_anh=payload.hinh_anh,
        gia=payload.gia,
        gia_goc=payload.gia_goc,
        so_buoi=payload.so_buoi,
        thoi_luong=payload.thoi_luong,
        hinh_thuc=payload.hinh_thuc,
        teacher_id=payload.teacher_id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

