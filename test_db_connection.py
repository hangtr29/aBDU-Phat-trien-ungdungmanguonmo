#!/usr/bin/env python3
"""Script test kết nối database"""
import sys
from pathlib import Path

# Thêm fastapi_app vào path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from fastapi_app.core.config import settings
    from fastapi_app.db.session import SessionLocal
    
    print("=" * 50)
    print("KIEM TRA KET NOI DATABASE")
    print("=" * 50)
    
    # Kiểm tra config
    print(f"\n1. Database URL: {settings.database_url[:50]}...")
    print(f"2. JWT Secret: {'OK' if settings.jwt_secret else 'MISSING'}")
    
    # Test kết nối
    print("\n3. Dang test ket noi database...")
    db = SessionLocal()
    try:
        # Test query đơn giản
        from sqlalchemy import text
        result = db.execute(text("SELECT 1")).scalar()
        print(f"   [OK] Ket noi thanh cong! (result: {result})")
        
        # Kiểm tra bảng users
        print("\n4. Kiem tra bang users...")
        user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
        print(f"   So luong users: {user_count}")
        
        if user_count > 0:
            # Lấy danh sách users
            users = db.execute(text("SELECT email, role FROM users LIMIT 5")).fetchall()
            print("\n   Danh sach users:")
            for email, role in users:
                print(f"   - {email} ({role})")
        else:
            print("   [WARNING] CHUA CO USER! Can chay seed data:")
            print("      .\\scripts\\setup-database.ps1")
            
    except Exception as e:
        print(f"   [ERROR] Loi ket noi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        
    print("\n" + "=" * 50)
    
except Exception as e:
    print(f"[ERROR] Loi: {e}")
    import traceback
    traceback.print_exc()

