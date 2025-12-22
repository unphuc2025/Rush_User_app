#!/usr/bin/env python3
"""
Test booking creation directly with database to isolate the issue
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from sqlalchemy import text
import uuid

def test_direct_insert():
    """Test inserting a booking directly to find the exact error"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("TESTING DIRECT BOOKING INSERT")
        print("=" * 60)
        
        # First, get a real user_id and court_id from database
        print("\n1. Getting existing user ID...")
        user_result = db.execute(text("SELECT id FROM users LIMIT 1"))
        user_row = user_result.fetchone()
        
        if not user_row:
            print("❌ No users found in database!")
            return
        
        user_id = user_row[0]
        print(f"✅ Found user: {user_id} (type: {type(user_id)})")
        
        print("\n2. Getting existing court ID from venues or admin_courts...")
        # Try venues first
        court_result = db.execute(text("SELECT id FROM venues LIMIT 1"))
        court_row = court_result.fetchone()
        
        if not court_row:
            # Try admin_courts
            print("   No venues found, trying admin_courts...")
            court_result = db.execute(text("SELECT id FROM admin_courts LIMIT 1"))
            court_row = court_result.fetchone()
        
        if not court_row:
            print("❌ No courts found in database!")
            return
        
        court_id = court_row[0]
        print(f"✅ Found court: {court_id} (type: {type(court_id)})")
        
        print("\n3. Attempting to insert booking...")
        
        # Try inserting with explicit values
        insert_sql = """
            INSERT INTO booking (
                user_id, court_id, booking_date, start_time, end_time,
                duration_minutes, number_of_players, price_per_hour, 
                total_amount, status, payment_status
            ) VALUES (
                :user_id, :court_id, :booking_date, :start_time, :end_time,
                :duration_minutes, :number_of_players, :price_per_hour,
                :total_amount, :status, :payment_status
            )
            RETURNING id;
        """
        
        params = {
            'user_id': user_id,
            'court_id': court_id,
            'booking_date': '2025-11-24',
            'start_time': '10:00:00',
            'end_time': '11:00:00',
            'duration_minutes': 60,
            'number_of_players': 2,
            'price_per_hour': 201.00,
            'total_amount': 402.00,
            'status': 'pending',
            'payment_status': 'pending'
        }
        
        print(f"\n📝 Test booking data:")
        for key, value in params.items():
            print(f"   {key}: {value} (type: {type(value).__name__})")
        
        result = db.execute(text(insert_sql), params)
        new_id = result.fetchone()[0]
        db.commit()
        
        print(f"\n✅ SUCCESS! Booking created with ID: {new_id}")
        print("=" * 60)
        print("🎯 DATABASE INSERT WORKS!")
        print("=" * 60)
        print("\n⚠️  If this works but API doesn't, the issue is in:")
        print("   1. FastAPI route registration")
        print("   2. Pydantic schema validation")
        print("   3. CRUD function logic")
        print("   4. Authentication middleware")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n📋 Error Details:")
        import traceback
        traceback.print_exc()
        
        print("\n💡 Common Causes:")
        print("   1. Foreign key constraint: court_id not in venues table")
        print("   2. Type mismatch: user_id/court_id string vs UUID")
        print("   3. Missing required fields")
        print("   4. Invalid date/time format")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_direct_insert()
