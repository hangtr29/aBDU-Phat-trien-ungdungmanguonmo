from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List
from decimal import Decimal
from datetime import datetime

from ...db.session import get_db
from ...api.deps import get_current_admin_user
from ...models.user import User
from ...models.deposit import DepositTransaction, DepositStatus
from ...models.payment import Payment, PaymentStatus
from ...models.course import Course
from ...models.notification import Notification
from ...schemas.wallet import DepositTransactionOut

router = APIRouter()


@router.get("/deposits/pending", response_model=List[DepositTransactionOut])
def get_pending_deposits(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Lấy danh sách giao dịch nạp tiền chờ duyệt"""
    transactions = db.query(DepositTransaction).filter(
        DepositTransaction.trang_thai == DepositStatus.pending
    ).order_by(DepositTransaction.created_at.desc()).all()
    
    # Thêm thông tin user
    result = []
    for t in transactions:
        user = db.query(User).filter(User.id == t.user_id).first()
        result.append(DepositTransactionOut(
            id=t.id,
            user_id=t.user_id,
            so_tien=t.so_tien,
            noi_dung_chuyen_khoan=t.noi_dung_chuyen_khoan,
            trang_thai=t.trang_thai,
            ma_giao_dich=t.ma_giao_dich,
            ghi_chu=t.ghi_chu,
            created_at=t.created_at,
            updated_at=t.updated_at,
            ngay_duyet=t.ngay_duyet,
            nguoi_duyet_id=t.nguoi_duyet_id,
            user_email=user.email if user else None,
            user_name=user.ho_ten if user else None
        ))
    
    return result


@router.post("/deposits/{transaction_id}/approve")
def approve_deposit(
    transaction_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Duyệt giao dịch nạp tiền - cộng tiền vào tài khoản user"""
    transaction = db.query(DepositTransaction).filter(
        DepositTransaction.id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy giao dịch"
        )
    
    if transaction.trang_thai != DepositStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Giao dịch đã được xử lý (trạng thái: {transaction.trang_thai})"
        )
    
    # Cập nhật trạng thái
    transaction.trang_thai = DepositStatus.completed
    transaction.ngay_duyet = datetime.utcnow()
    transaction.nguoi_duyet_id = admin.id
    transaction.ma_giao_dich = f"DEPOSIT_{transaction_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Cộng tiền vào tài khoản user
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if user:
        user.so_du = (user.so_du or Decimal("0")) + transaction.so_tien
        
        # Tạo thông báo cho user
        so_tien_str = f"{float(transaction.so_tien):,.0f}".replace(',', '.')
        so_du_str = f"{float(user.so_du):,.0f}".replace(',', '.')
        notification = Notification(
            user_id=user.id,
            loai="deposit",
            tieu_de="Nạp tiền thành công",
            noi_dung=f"Giao dịch nạp tiền {so_tien_str} VNĐ đã được duyệt. Số dư hiện tại: {so_du_str} VNĐ",
            link="/addfunds"
        )
        db.add(notification)
    
    db.commit()
    db.refresh(transaction)
    
    return {
        "message": "Đã duyệt giao dịch thành công",
        "transaction": transaction,
        "so_du_moi": user.so_du if user else None
    }


@router.post("/deposits/{transaction_id}/reject")
def reject_deposit(
    transaction_id: int,
    ghi_chu: str = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Từ chối giao dịch nạp tiền"""
    transaction = db.query(DepositTransaction).filter(
        DepositTransaction.id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy giao dịch"
        )
    
    if transaction.trang_thai != DepositStatus.pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Giao dịch đã được xử lý (trạng thái: {transaction.trang_thai})"
        )
    
    # Cập nhật trạng thái
    transaction.trang_thai = DepositStatus.failed
    transaction.ngay_duyet = datetime.utcnow()
    transaction.nguoi_duyet_id = admin.id
    if ghi_chu:
        transaction.ghi_chu = ghi_chu
    
    # Tạo thông báo cho user
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if user:
        so_tien_str = f"{float(transaction.so_tien):,.0f}".replace(',', '.')
        notification = Notification(
            user_id=user.id,
            loai="deposit",
            tieu_de="Thanh toán không thành công",
            noi_dung=f"Giao dịch nạp tiền {so_tien_str} VNĐ đã bị từ chối. {ghi_chu if ghi_chu else 'Vui lòng kiểm tra lại thông tin chuyển khoản.'}",
            link="/addfunds"
        )
        db.add(notification)
    
    db.commit()
    db.refresh(transaction)
    
    return {
        "message": "Đã từ chối giao dịch",
        "transaction": transaction
    }


@router.get("/revenue/by-course")
def get_revenue_by_course(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Tính tổng doanh thu từng khóa học"""
    # Lấy doanh thu từ các payment đã hoàn thành
    revenue_by_course = db.query(
        Course.id,
        Course.tieu_de,
        func.sum(Payment.so_tien).label('tong_doanh_thu'),
        func.count(Payment.id).label('so_luong_giao_dich')
    ).join(
        Payment, Course.id == Payment.khoa_hoc_id
    ).filter(
        Payment.trang_thai == PaymentStatus.completed
    ).group_by(
        Course.id, Course.tieu_de
    ).all()
    
    result = []
    for course_id, tieu_de, tong_doanh_thu, so_luong in revenue_by_course:
        result.append({
            "khoa_hoc_id": course_id,
            "tieu_de": tieu_de,
            "tong_doanh_thu": float(tong_doanh_thu) if tong_doanh_thu else 0,
            "so_luong_giao_dich": so_luong
        })
    
    return result


@router.get("/revenue/total")
def get_total_revenue(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Tính tổng doanh thu từ các giao dịch nạp tiền đã được duyệt"""
    # Tính tổng từ các giao dịch nạp tiền đã được duyệt (completed)
    total = db.query(func.sum(DepositTransaction.so_tien)).filter(
        DepositTransaction.trang_thai == DepositStatus.completed
    ).scalar()
    
    total_count = db.query(func.count(DepositTransaction.id)).filter(
        DepositTransaction.trang_thai == DepositStatus.completed
    ).scalar()
    
    return {
        "tong_doanh_thu": float(total) if total else 0,
        "tong_so_giao_dich": total_count or 0
    }


@router.get("/deposits/all", response_model=List[DepositTransactionOut])
def get_all_deposits(
    trang_thai: str = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Lấy tất cả giao dịch nạp tiền (admin)"""
    query = db.query(DepositTransaction)
    
    if trang_thai:
        query = query.filter(DepositTransaction.trang_thai == trang_thai)
    
    transactions = query.order_by(DepositTransaction.created_at.desc()).all()
    return transactions









