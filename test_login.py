#!/usr/bin/env python3
"""Test login API"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi_app.api.routes.auth import login
from fastapi_app.schemas.auth import LoginRequest
from fastapi_app.db.session import SessionLocal
from fastapi import BackgroundTasks

print("Testing login function...")

try:
    # Test với admin
    payload = LoginRequest(email="admin@example.com", password="admin123")
    db = SessionLocal()
    background_tasks = BackgroundTasks()
    
    result = login(payload, db)
    print(f"[OK] Login successful!")
    print(f"Token: {result.access_token[:50]}...")
    db.close()
except Exception as e:
    print(f"[ERROR] Login failed: {e}")
    import traceback
    traceback.print_exc()









