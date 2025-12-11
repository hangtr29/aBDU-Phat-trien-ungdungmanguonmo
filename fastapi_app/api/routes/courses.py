from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ...db.session import get_db
from ...models.course import Course, CourseStatus, CourseMode
from ...schemas.course import CourseCreate, CourseOut

router = APIRouter()


@router.get("/courses", response_model=list[CourseOut])
def list_courses(
    q: str | None = Query(None, description="Tìm theo tiêu đề/mô tả"),
    cap_do: str | None = Query(None, description="Lọc cấp độ (Beginner/Intermediate/Advanced)"),
    hinh_thuc: CourseMode | None = Query(None, description="online/offline/hybrid"),
    status: CourseStatus | None = Query(None, description="active/inactive/draft"),
    sort: str | None = Query("newest", description="newest|price_asc|price_desc"),
    db: Session = Depends(get_db),
):
    query = db.query(Course)

    if status:
        query = query.filter(Course.trang_thai == status)
    else:
        # Mặc định chỉ trả active
        query = query.filter(Course.trang_thai == CourseStatus.active)

    if cap_do:
        query = query.filter(Course.cap_do == cap_do)

    if hinh_thuc:
        query = query.filter(Course.hinh_thuc == hinh_thuc)

    if q:
        like_q = f"%{q}%"
        query = query.filter(or_(Course.tieu_de.ilike(like_q), Course.mo_ta.ilike(like_q)))

    if sort == "price_asc":
        query = query.order_by(Course.gia.asc())
    elif sort == "price_desc":
        query = query.order_by(Course.gia.desc())
    else:
        query = query.order_by(Course.created_at.desc())

    return query.all()


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

