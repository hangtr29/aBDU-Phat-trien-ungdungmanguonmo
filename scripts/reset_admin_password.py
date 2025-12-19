#!/usr/bin/env python3
"""Script reset password cho admin"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi_app.db.session import SessionLocal
from fastapi_app.models.user import User, UserRole
from fastapi_app.core.security import hash_password

def reset_admin_password(new_password: str = "admin123"):
    """Reset password cho tất cả admin accounts"""
    db = SessionLocal()
    try:
        # Tìm tất cả admin accounts
        admins = db.query(User).filter(User.role == UserRole.admin).all()
        
        if not admins:
            print("[WARNING] Không tìm thấy tài khoản admin nào!")
            return
        
        print(f"[INFO] Tìm thấy {len(admins)} tài khoản admin:")
        for admin in admins:
            print(f"  - {admin.email} (ID: {admin.id})")
        
        # Reset password cho tất cả admin
        password_hash = hash_password(new_password)
        
        for admin in admins:
            admin.password_hash = password_hash
            print(f"[OK] Đã reset password cho {admin.email}")
        
        db.commit()
        print(f"\n[SUCCESS] Đã reset password cho {len(admins)} tài khoản admin!")
        print(f"[INFO] Password mới: {new_password}")
        print("\nTài khoản admin:")
        for admin in admins:
            print(f"  - Email: {admin.email}")
            print(f"    Password: {new_password}")
        
    except Exception as e:
        print(f"[ERROR] Lỗi: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Reset password cho admin")
    parser.add_argument(
        "--password",
        type=str,
        default="admin123",
        help="Password mới (mặc định: admin123)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("RESET PASSWORD CHO ADMIN")
    print("=" * 60)
    print(f"\nPassword mới sẽ là: {args.password}")
    confirm = input("\nBạn có chắc muốn tiếp tục? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y', 'có']:
        reset_admin_password(args.password)
    else:
        print("[CANCELLED] Đã hủy.")

