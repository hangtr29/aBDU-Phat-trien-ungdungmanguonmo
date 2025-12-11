from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import uuid
from datetime import datetime, timedelta

from ...db.session import get_db
from ...models.payment import Payment, PaymentStatus, PaymentMethod
from ...models.course import Course
from ...models.enrollment import Enrollment
from ...schemas.payment import PaymentCreate, PaymentOut, PaymentCallback, PaymentLinkResponse
from ...api.deps import get_current_active_user
from ...models.user import User

router = APIRouter()


def generate_order_id() -> str:
    """Tạo mã đơn hàng unique"""
    return f"ORDER_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8].upper()}"


@router.post("/create", response_model=PaymentLinkResponse)
def create_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Tạo đơn hàng và payment link"""
    # Kiểm tra khóa học tồn tại
    course = db.query(Course).filter(Course.id == payload.khoa_hoc_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khóa học không tồn tại"
        )

    # Kiểm tra khóa học có phí không
    if course.gia and course.gia > 0:
        if payload.so_tien != course.gia:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Số tiền không khớp. Giá khóa học: {course.gia}"
            )
    else:
        # Khóa học miễn phí, không cần thanh toán
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khóa học này miễn phí, không cần thanh toán"
        )

    # Kiểm tra đã đăng ký chưa
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.khoa_hoc_id == payload.khoa_hoc_id,
        Enrollment.trang_thai == 'active'
    ).first()
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bạn đã đăng ký khóa học này rồi"
        )

    # Tạo mã đơn hàng
    ma_don_hang = generate_order_id()

    # Tạo payment record
    payment = Payment(
        user_id=current_user.id,
        khoa_hoc_id=payload.khoa_hoc_id,
        so_tien=payload.so_tien,
        phuong_thuc=payload.phuong_thuc,
        trang_thai=PaymentStatus.pending,
        ma_don_hang=ma_don_hang
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Tạo payment URL (giả lập, sẽ tích hợp với cổng thanh toán thật sau)
    # TODO: Tích hợp với Momo/ZaloPay/PayPal API
    payment_url = f"/payment/process/{payment.id}?method={payload.phuong_thuc.value}"

    return PaymentLinkResponse(
        payment_url=payment_url,
        ma_don_hang=ma_don_hang,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )


@router.post("/callback", response_model=PaymentOut)
def payment_callback(
    payload: PaymentCallback,
    db: Session = Depends(get_db)
):
    """Xử lý callback từ cổng thanh toán"""
    # Tìm payment theo mã đơn hàng
    payment = db.query(Payment).filter(
        Payment.ma_don_hang == payload.ma_don_hang
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn hàng"
        )

    # Cập nhật thông tin giao dịch
    payment.ma_giao_dich = payload.ma_giao_dich
    if payload.thong_tin_them:
        payment.thong_tin_them = payload.thong_tin_them

    # Xử lý theo trạng thái
    if payload.trang_thai == "success":
        payment.trang_thai = PaymentStatus.completed
        payment.ngay_thanh_toan = datetime.utcnow()

        # Tự động đăng ký khóa học
        enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == payment.user_id,
            Enrollment.khoa_hoc_id == payment.khoa_hoc_id
        ).first()

        if not enrollment:
            enrollment = Enrollment(
                user_id=payment.user_id,
                khoa_hoc_id=payment.khoa_hoc_id,
                trang_thai='active'
            )
            db.add(enrollment)
        else:
            enrollment.trang_thai = 'active'

    elif payload.trang_thai == "failed":
        payment.trang_thai = PaymentStatus.failed
    elif payload.trang_thai == "cancelled":
        payment.trang_thai = PaymentStatus.cancelled

    db.commit()
    db.refresh(payment)

    return payment


@router.get("/me", response_model=list[PaymentOut])
def get_my_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy danh sách thanh toán của user hiện tại"""
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).order_by(Payment.created_at.desc()).all()
    return payments


@router.post("/demo-complete", response_model=PaymentOut)
def demo_complete_payment(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Endpoint demo: Tự động hoàn thành thanh toán (chỉ dùng cho demo/testing)"""
    ma_don_hang = payload.get("ma_don_hang")
    if not ma_don_hang:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Thiếu mã đơn hàng"
        )

    # Tìm payment
    payment = db.query(Payment).filter(
        Payment.ma_don_hang == ma_don_hang,
        Payment.user_id == current_user.id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy đơn hàng"
        )

    if payment.trang_thai == PaymentStatus.completed:
        # Đã thanh toán rồi, trả về luôn
        return payment

    # Giả lập thanh toán thành công
    payment.trang_thai = PaymentStatus.completed
    payment.ma_giao_dich = f"DEMO_{ma_don_hang}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    payment.ngay_thanh_toan = datetime.utcnow()

    # Tự động đăng ký khóa học
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == payment.user_id,
        Enrollment.khoa_hoc_id == payment.khoa_hoc_id
    ).first()

    if not enrollment:
        enrollment = Enrollment(
            user_id=payment.user_id,
            khoa_hoc_id=payment.khoa_hoc_id,
            trang_thai='active'
        )
        db.add(enrollment)
    else:
        enrollment.trang_thai = 'active'

    db.commit()
    db.refresh(payment)

    return payment


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy chi tiết một payment"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thanh toán"
        )

    # Chỉ cho phép xem payment của chính mình hoặc admin
    if payment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xem thanh toán này"
        )

    return payment

