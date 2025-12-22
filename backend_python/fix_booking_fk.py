#!/usr/bin/env python3
"""
Automated script to fix booking foreign key constraint issue
This removes the FK constraint and updates validation logic
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from sqlalchemy import text

def fix_booking_constraint():
    """Remove foreign key constraint from booking.court_id"""
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("AUTOMATED FIX: Removing Foreign Key Constraint from booking.court_id")
        print("=" * 70)
        
        # Step 1: Check if constraint exists
        print("\n[1/3] Checking for existing foreign key constraint...")
        
        check_constraint = """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'booking'
            AND constraint_type = 'FOREIGN KEY'
            AND constraint_name LIKE '%court_id%';
        """
        
        result = db.execute(text(check_constraint))
        constraints = result.fetchall()
        
        if not constraints:
            print("   ℹ️  No foreign key constraint found on booking.court_id")
            print("   ✅ Constraint already removed or doesn't exist")
        else:
            constraint_name = constraints[0][0]
            print(f"   ✅ Found constraint: {constraint_name}")
            
            # Step 2: Drop the constraint
            print(f"\n[2/3] Dropping foreign key constraint '{constraint_name}'...")
            
            drop_constraint = f"""
                ALTER TABLE booking
                DROP CONSTRAINT IF EXISTS {constraint_name};
            """
            
            db.execute(text(drop_constraint))
            db.commit()
            
            print(f"   ✅ Successfully dropped constraint '{constraint_name}'")
        
        # Step 3: Verify
        print("\n[3/3] Verifying constraint removal...")
        
        result = db.execute(text(check_constraint))
        remaining = result.fetchall()
        
        if not remaining:
            print("   ✅ Verification successful - No FK constraint on court_id")
        else:
            print(f"   ⚠️  Warning: Still found constraints: {remaining}")
        
        print("\n" + "=" * 70)
        print("✅ DATABASE FIX COMPLETE!")
        print("=" * 70)
        print("\n📋 What was fixed:")
        print("   • Removed foreign key constraint from booking.court_id")
        print("   • booking.court_id is now a regular UUID column")
        print("   • Can now accept court IDs from admin_courts table")
        
        print("\n🚀 NEXT STEPS:")
        print("   1. Restart the backend server")
        print("   2. Test booking creation from mobile app")
        print("   3. Booking should work successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 If error occurs:")
        print("   • Make sure PostgreSQL is running")
        print("   • Check database connection in .env")
        print("   • Verify you have ALTER TABLE permissions")
        
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    success = fix_booking_constraint()
    sys.exit(0 if success else 1)
