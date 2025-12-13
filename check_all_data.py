#!/usr/bin/env python3
"""Script kiem tra tat ca du lieu trong database"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.db.session import SessionLocal
from sqlalchemy import text

print("=" * 60)
print("KIEM TRA TAT CA DU LIEU DATABASE")
print("=" * 60)

db = SessionLocal()
try:
    # Lấy danh sách tất cả các bảng
    tables_query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    ORDER BY table_name;
    """
    
    tables = db.execute(text(tables_query)).fetchall()
    
    print(f"\nTong so bang: {len(tables)}\n")
    
    total_records = 0
    empty_tables = []
    
    for (table_name,) in tables:
        try:
            count_query = f"SELECT COUNT(*) FROM {table_name}"
            count = db.execute(text(count_query)).scalar()
            total_records += count
            
            status = "[OK]" if count > 0 else "[EMPTY]"
            print(f"{status} {table_name:30s} : {count:5d} records")
            
            if count == 0:
                empty_tables.append(table_name)
                
        except Exception as e:
            print(f"[ERROR] {table_name:30s} : {str(e)[:50]}")
    
    print("\n" + "=" * 60)
    print(f"Tong so records: {total_records}")
    print("=" * 60)
    
    if empty_tables:
        print(f"\n[WARNING] Co {len(empty_tables)} bang chua co du lieu:")
        for table in empty_tables:
            print(f"  - {table}")
        print("\nCan chay seed data:")
        print("  .\\scripts\\setup-database.ps1")
    else:
        print("\n[OK] Tat ca cac bang deu co du lieu!")
    
    # Kiểm tra các bảng quan trọng
    print("\n" + "=" * 60)
    print("CHI TIET CAC BANG QUAN TRONG")
    print("=" * 60)
    
    important_tables = {
        'users': 'Tai khoan',
        'khoa_hoc': 'Khoa hoc',
        'chi_tiet_khoa_hoc': 'Bai hoc',
        'bai_tap': 'Bai tap',
        'dang_ky_khoa_hoc': 'Dang ky khoa hoc',
        'tien_do_hoc_tap': 'Tien do',
    }
    
    for table, desc in important_tables.items():
        try:
            count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"{desc:20s} ({table:25s}): {count:5d}")
        except:
            print(f"{desc:20s} ({table:25s}): KHONG TON TAI")
    
except Exception as e:
    print(f"[ERROR] Loi: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

