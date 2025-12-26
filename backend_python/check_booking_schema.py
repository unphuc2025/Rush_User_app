#!/usr/bin/env python3
"""
Check the booking table schema in PostgreSQL database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from sqlalchemy import text

def check_booking_table():
    """Check booking table schema"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("CHECKING BOOKING TABLE SCHEMA IN DATABASE")
        print("=" * 60)
        
        # Check if table exists
        table_check = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'booking'
            );
        """
        result = db.execute(text(table_check))
        table_exists = result.scalar()
        
        if not table_exists:
            print("❌ ERROR: 'booking' table does NOT exist in database!")
            print("\nChecking for 'bookings' table (plural)...")
            
            table_check_plural = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'bookings'
                );
            """
            result = db.execute(text(table_check_plural))
            bookings_exists = result.scalar()
            
            if bookings_exists:
                print("✅ Found 'bookings' table (plural)")
                print("\n⚠️  FIX REQUIRED: Update models.py to use 'bookings' not 'booking'")
            else:
                print("❌ Neither 'booking' nor 'bookings' table exists!")
            
            return
        
        print("✅ 'booking' table exists\n")
        
        # Get all columns from booking table
        columns_query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'booking'
            ORDER BY ordinal_position;
        """
        
        result = db.execute(text(columns_query))
        columns = result.fetchall()
        
        print(f"📊 BOOKING TABLE COLUMNS ({len(columns)} total):")
        print("-" * 60)
        
        for col in columns:
            col_dict = dict(col._mapping)
            nullable = "NULL" if col_dict['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT: {col_dict['column_default']}" if col_dict['column_default'] else ""
            print(f"  • {col_dict['column_name']:<20} {col_dict['data_type']:<20} {nullable}{default}")
        
        print("\n" + "=" * 60)
        print("CHECKING FOR REQUIRED COLUMNS")
        print("=" * 60)
        
        required_columns = {
            'id': 'character varying',
            'user_id': 'character varying',
            'court_id': 'character varying',  # Should be court_id not venue_id
            'booking_date': 'date',
            'start_time': 'time without time zone',
            'end_time': 'time without time zone',
            'duration_minutes': 'integer',
            'number_of_players': 'integer',
            'price_per_hour': 'numeric',
            'total_amount': 'numeric',
            'status': 'character varying',
            'payment_status': 'character varying'
        }
        
        column_names = {col._mapping['column_name']: col._mapping['data_type'] for col in columns}
        
        all_good = True
        for req_col, req_type in required_columns.items():
            if req_col in column_names:
                actual_type = column_names[req_col]
                if req_type in actual_type or actual_type in req_type:
                    print(f"✅ {req_col:<20} - Found ({actual_type})")
                else:
                    print(f"⚠️  {req_col:<20} - Type mismatch: expected {req_type}, got {actual_type}")
                    all_good = False
            else:
                print(f"❌ {req_col:<20} - MISSING!")
                all_good = False
                
                # Check if venue_id exists instead of court_id
                if req_col == 'court_id' and 'venue_id' in column_names:
                    print(f"   ⚠️  Found 'venue_id' instead - MIGRATION NEEDED!")
                    print(f"   Run: ALTER TABLE booking RENAME COLUMN venue_id TO court_id;")
        
        print("\n" + "=" * 60)
        if all_good:
            print("✅ ALL REQUIRED COLUMNS PRESENT AND CORRECT")
        else:
            print("❌ SCHEMA ISSUES DETECTED - SEE ABOVE")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_booking_table()
