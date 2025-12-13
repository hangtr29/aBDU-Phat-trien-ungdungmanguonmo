from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from datetime import datetime
import secrets
import string

from ...db.session import get_db
from ...api.deps import get_current_active_user, get_current_admin_user
from ...models.user import User
from ...models.deposit import DepositTransaction, DepositStatus
from ...schemas.wallet import (
    AddFundsRequest, 
    AddFundsResponse, 
    WalletInfoResponse,
    QRCodeData,
    SubmitPaymentRequest,
    DepositTransactionOut
)

router = APIRouter()

# Thông tin tài khoản ngân hàng (cấu hình trong .env hoặc database)
BANK_ACCOUNT = {
    "stk": "0377070269",  # Số tài khoản từ QR code
    "ten_nguoi_nhan": "LE GIA BAO",  # Tên người nhận từ QR code
    "ten_ngan_hang": "Vietcombank"  # Có thể cập nhật theo ngân hàng thật
}


def generate_transfer_content(user_id: int) -> str:
    """Tạo nội dung chuyển khoản ngẫu nhiên"""
    # Format: NAPTIEN_{user_id}_{random_string}
    random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return f"NAPTIEN_{user_id}_{random_str}"


def generate_vietqr_data(amount: Decimal, content: str) -> str:
    """
    Tạo dữ liệu VietQR theo chuẩn
    Format: https://vietqr.net/soan-ma-qr?accountNo={stk}&accountName={ten}&amount={amount}&addInfo={content}
    """
    stk = BANK_ACCOUNT["stk"]
    ten = BANK_ACCOUNT["ten_nguoi_nhan"]
    amount_int = int(amount)
    
    # URL VietQR
    qr_data = f"https://vietqr.net/soan-ma-qr?accountNo={stk}&accountName={ten}&amount={amount_int}&addInfo={content}"
    
    return qr_data


@router.get("/balance", response_model=WalletInfoResponse)
def get_wallet_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy thông tin số dư ví"""
    return WalletInfoResponse(
        so_du=current_user.so_du or Decimal("0"),
        stk=BANK_ACCOUNT["stk"],
        ten_nguoi_nhan=BANK_ACCOUNT["ten_nguoi_nhan"]
    )


@router.post("/add-funds", response_model=AddFundsResponse)
def create_add_funds_request(
    payload: AddFundsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Tạo yêu cầu nạp tiền và trả về QR code"""
    
    # Validate số tiền
    if payload.so_tien < 50000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số tiền tối thiểu là 50,000 VNĐ"
        )
    
    if payload.so_tien != int(payload.so_tien):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ nhập số nguyên (không có phần thập phân)"
        )
    
    # Tạo nội dung chuyển khoản
    noi_dung = generate_transfer_content(current_user.id)
    
    # Tạo QR code data
    qr_data = generate_vietqr_data(payload.so_tien, noi_dung)
    
    return AddFundsResponse(
        stk=BANK_ACCOUNT["stk"],
        ten_nguoi_nhan=BANK_ACCOUNT["ten_nguoi_nhan"],
        ten_ngan_hang=BANK_ACCOUNT["ten_ngan_hang"],
        noi_dung_chuyen_khoan=noi_dung,
        so_tien=payload.so_tien,
        qr_code_data=qr_data
    )


@router.post("/submit-payment")
def submit_payment(
    payload: SubmitPaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """User báo đã thanh toán - tạo giao dịch chờ duyệt"""
    
    # Kiểm tra nội dung chuyển khoản có đúng format không
    if not payload.noi_dung_chuyen_khoan.startswith(f"NAPTIEN_{current_user.id}_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung chuyển khoản không hợp lệ"
        )
    
    # Kiểm tra đã có giao dịch với nội dung này chưa
    existing = db.query(DepositTransaction).filter(
        DepositTransaction.noi_dung_chuyen_khoan == payload.noi_dung_chuyen_khoan,
        DepositTransaction.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Giao dịch với nội dung này đã tồn tại"
        )
    
    # Validate số tiền
    if payload.so_tien < 50000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số tiền tối thiểu là 50,000 VNĐ"
        )
    
    # Tạo mã giao dịch
    ma_giao_dich = f"DEP_{current_user.id}_{secrets.token_hex(8)}"
    
    # Tạo giao dịch mới với trạng thái pending
    transaction = DepositTransaction(
        user_id=current_user.id,
        so_tien=payload.so_tien,
        ma_giao_dich=ma_giao_dich,
        noi_dung_chuyen_khoan=payload.noi_dung_chuyen_khoan,
        trang_thai=DepositStatus.pending
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return {
        "message": "Đã gửi yêu cầu nạp tiền. Vui lòng chờ admin duyệt từ 10-15 phút.",
        "transaction_id": transaction.id,
        "trang_thai": transaction.trang_thai.value
    }


@router.post("/verify-payment")
def verify_payment(
    noi_dung: str,
    so_tien: Decimal,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Xác thực thanh toán (sẽ được gọi khi admin xác nhận đã nhận tiền)
    Format noi_dung: NAPTIEN_{user_id}_{random_string}
    """
    if not noi_dung.startswith("NAPTIEN_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung chuyển khoản không hợp lệ"
        )
    
    # Parse user_id từ nội dung
    parts = noi_dung.split("_")
    if len(parts) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung chuyển khoản không hợp lệ"
        )
    
    try:
        user_id_from_content = int(parts[1])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nội dung chuyển khoản không hợp lệ"
        )
    
    # Chỉ cho phép user xác thực thanh toán của chính mình
    if user_id_from_content != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xác thực thanh toán này"
        )
    
    # Cập nhật số dư
    current_user.so_du = (current_user.so_du or Decimal("0")) + so_tien
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Nạp tiền thành công",
        "so_du_moi": current_user.so_du
    }

