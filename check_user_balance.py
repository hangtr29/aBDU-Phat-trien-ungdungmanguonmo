#!/usr/bin/env python3
"""Kiem tra cot so_du trong bang users"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    # Kiem tra cot so_du co ton tai khong
    result = db.execute(text("""
        SELECT column_name, data_type, column_default
        FROM information_schema.columns
        WHERE table_name = 'users' AND column_name = 'so_du'
    """)).fetchall()
    
    if result:
        print("[OK] Cot so_du da ton tai trong bang users")
        for row in result:
            print(f"  - Column: {row[0]}, Type: {row[1]}, Default: {row[2]}")
    else:
        print("[ERROR] Cot so_du CHUA ton tai!")
        print("Can chay migration: database/add_user_balance.sql")
        
    # Kiem tra gia tri so_du cua users
    print("\nKiem tra so_du cua cac users:")
    users = db.execute(text("SELECT id, email, so_du FROM users LIMIT 5")).fetchall()
    for user_id, email, so_du in users:
        print(f"  - {email}: so_du = {so_du}")
        
except Exception as e:
    print(f"[ERROR] Loi: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

