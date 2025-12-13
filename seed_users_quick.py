#!/usr/bin/env python3
"""Script seed users nhanh"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.db.session import SessionLocal
from sqlalchemy import text

print("Dang seed users...")

db = SessionLocal()
try:
    # Đọc file seed_users.sql
    seed_file = Path(__file__).parent / "database" / "seed_users.sql"
    sql_content = seed_file.read_text(encoding='utf-8')
    
    # Chạy SQL
    db.execute(text(sql_content))
    db.commit()
    
    # Kiểm tra kết quả
    user_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar()
    print(f"[OK] Da seed thanh cong! So luong users: {user_count}")
    
    # Hiển thị danh sách users
    users = db.execute(text("SELECT email, role FROM users")).fetchall()
    print("\nDanh sach users:")
    for email, role in users:
        print(f"  - {email} ({role})")
    
    print("\nTai khoan test:")
    print("  - Admin: admin@example.com / admin123")
    print("  - Teacher: teacher1@example.com / teacher123")
    print("  - Student: student@example.com / student123")
    
except Exception as e:
    print(f"[ERROR] Loi: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()

