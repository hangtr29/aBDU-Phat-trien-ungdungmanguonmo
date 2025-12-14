#!/usr/bin/env python3
"""
Script để chạy tất cả migrations trên database
Sử dụng khi deploy lên production
"""
import os
import sys
from pathlib import Path
import psycopg

# Thêm thư mục root vào path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL environment variable not set")
    sys.exit(1)

# Chuyển đổi DATABASE_URL từ format SQLAlchemy sang psycopg
# postgresql+psycopg://... -> postgresql://...
if DATABASE_URL.startswith("postgresql+psycopg"):
    DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")

print(f"📦 Connecting to database...")
print(f"   Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'hidden'}")

try:
    # Kết nối database
    conn = psycopg.connect(DATABASE_URL)
    cur = conn.cursor()
    print("✅ Connected to database successfully\n")

    # Danh sách các file migration (theo thứ tự)
    migration_files = [
        "database/schema_pg.sql",
        "database/create_enrollment_table.sql",
        "database/create_notifications_table.sql",
        "database/create_payments_table.sql",
        "database/add_tai_lieu_to_lessons.sql",
        "database/add_diem_toi_da_to_assignments.sql",
        "database/create_deposit_transactions.sql",
        "database/add_deposit_fields.sql",
        "database/add_user_balance.sql",
    ]

    success_count = 0
    failed_count = 0

    for file_path in migration_files:
        full_path = project_root / file_path
        
        if not full_path.exists():
            print(f"⚠️  SKIP: {file_path} (file not found)")
            continue

        print(f"🔄 Running: {file_path}...")
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                sql = f.read()
                
            # Chạy SQL (chia nhỏ nếu có nhiều câu lệnh)
            statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]
            
            for statement in statements:
                if statement:
                    cur.execute(statement)
            
            conn.commit()
            print(f"   ✅ Completed: {file_path}")
            success_count += 1
        except Exception as e:
            # Một số lệnh có thể fail nếu đã chạy rồi (như CREATE TABLE IF NOT EXISTS)
            error_msg = str(e).lower()
            if "already exists" in error_msg or "duplicate" in error_msg:
                print(f"   ⚠️  Skipped (already exists): {file_path}")
                success_count += 1
            else:
                print(f"   ❌ ERROR in {file_path}: {e}")
                failed_count += 1
                conn.rollback()

    cur.close()
    conn.close()

    print("\n" + "="*50)
    print(f"📊 Migration Summary:")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {failed_count}")
    print("="*50)

    if failed_count > 0:
        print("\n⚠️  Some migrations failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n🎉 All migrations completed successfully!")
        sys.exit(0)

except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

