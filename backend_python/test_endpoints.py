#!/usr/bin/env python
import sys
import traceback

try:
    print("[TEST] Starting imports...")
    from database import get_db, SessionLocal
    print("[TEST] database OK")
    
    print("[TEST] Testing DB connection...")
    db = SessionLocal()
    print(f"[TEST] SessionLocal: {db}")
    db.close()
    print("[TEST] DB connection test OK")
    
    print("[TEST] Importing auth router...")
    from routers import auth
    print("[TEST] auth OK")
    
    print("[TEST] Creating test payload...")
    from schemas import SendOTPRequest
    payload = SendOTPRequest(phone_number="+919876543210")
    print(f"[TEST] Payload: {payload}")
    
    print("[TEST] Calling send_otp endpoint...")
    db = SessionLocal()
    result = auth.send_otp(payload, db)
    db.close()
    print(f"[TEST] Result: {result}")
    
    print("[TEST] ✓ ALL TESTS PASSED")
    
except Exception as e:
    print(f"[TEST] ✗ ERROR: {type(e).__name__}: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
