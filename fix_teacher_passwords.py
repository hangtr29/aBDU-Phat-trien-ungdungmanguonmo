#!/usr/bin/env python3
"""Fix teacher account passwords"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.db.session import SessionLocal
from fastapi_app.models.user import User
from fastapi_app.core.security import hash_password, verify_password

print("Dang kiem tra va sua password cho teacher accounts...")

db = SessionLocal()
try:
    teachers = db.query(User).filter(User.role == 'teacher').all()
    
    print(f"Tim thay {len(teachers)} teacher accounts:")
    
    for teacher in teachers:
        print(f"\n  - {teacher.email}:")
        
        # Test password hien tai
        test_result = False
        if teacher.password_hash:
            try:
                test_result = verify_password('teacher123', teacher.password_hash)
                print(f"    Password hash hien tai: {teacher.password_hash[:50]}...")
                print(f"    Test password 'teacher123': {'OK' if test_result else 'FAILED'}")
            except Exception as e:
                print(f"    Password hash bi loi format: {e}")
                test_result = False
        
        if not test_result:
            # Cap nhat password
            teacher.password_hash = hash_password('teacher123')
            print(f"    -> Da cap nhat password hash")
    
    db.commit()
    print("\n[OK] Da cap nhat tat ca teacher accounts!")
    
except Exception as e:
    print(f"[ERROR] Loi: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()









