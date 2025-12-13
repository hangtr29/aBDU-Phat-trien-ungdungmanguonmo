#!/usr/bin/env python3
"""Script seed tat ca du lieu"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.db.session import SessionLocal
from sqlalchemy import text

print("=" * 60)
print("SEED TAT CA DU LIEU")
print("=" * 60)

db = SessionLocal()
try:
    seed_files = [
        ("database/seed_programming_courses_fixed_utf8.sql", "Courses va Teachers"),
        ("database/seed_users.sql", "Users (neu chua co)"),
        ("database/seed_lesson_resources.sql", "Tai lieu bai hoc"),
    ]
    
    for seed_file, desc in seed_files:
        file_path = Path(__file__).parent / seed_file
        if not file_path.exists():
            print(f"\n[SKIP] {desc}: File khong ton tai")
            continue
            
        print(f"\nDang seed: {desc}...")
        try:
            sql_content = file_path.read_text(encoding='utf-8')
            db.execute(text(sql_content))
            db.commit()
            print(f"[OK] {desc}: Thanh cong!")
        except Exception as e:
            print(f"[ERROR] {desc}: {str(e)[:100]}")
            db.rollback()
            # Tiếp tục với file tiếp theo
            continue
    
    # Kiểm tra kết quả
    print("\n" + "=" * 60)
    print("KET QUA SAU KHI SEED")
    print("=" * 60)
    
    results = {
        'users': 'SELECT COUNT(*) FROM users',
        'khoa_hoc': 'SELECT COUNT(*) FROM khoa_hoc',
        'chi_tiet_khoa_hoc': 'SELECT COUNT(*) FROM chi_tiet_khoa_hoc',
        'bai_tap': 'SELECT COUNT(*) FROM bai_tap',
    }
    
    for name, query in results.items():
        try:
            count = db.execute(text(query)).scalar()
            print(f"{name:25s}: {count:5d}")
        except:
            print(f"{name:25s}: KHONG TON TAI")
    
    print("\n[OK] Hoan thanh!")
    
except Exception as e:
    print(f"\n[ERROR] Loi: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()

