#!/usr/bin/env python3
"""Chay migration de them cot so_du"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.db.session import SessionLocal
from sqlalchemy import text

print("Dang chay migration them cot so_du...")

db = SessionLocal()
try:
    # Kiem tra cot da ton tai chua
    check = db.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'so_du'
    """)).fetchone()
    
    if check:
        print("[INFO] Cot so_du da ton tai, khong can them")
    else:
        print("[INFO] Dang them cot so_du...")
        db.execute(text("""
            ALTER TABLE users 
            ADD COLUMN so_du NUMERIC(12, 2) DEFAULT 0 NOT NULL
        """))
        db.commit()
        print("[OK] Da them cot so_du thanh cong!")
        
        # Cap nhat so_du = 0 cho cac user hien tai neu chua co
        db.execute(text("""
            UPDATE users 
            SET so_du = 0 
            WHERE so_du IS NULL
        """))
        db.commit()
        print("[OK] Da cap nhat so_du = 0 cho tat ca users")
    
    # Kiem tra ket qua
    result = db.execute(text("SELECT COUNT(*) FROM users WHERE so_du IS NOT NULL")).scalar()
    print(f"[OK] So luong users co so_du: {result}")
    
except Exception as e:
    print(f"[ERROR] Loi: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()

