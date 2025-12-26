#!/usr/bin/env python3
"""
Test database connection for MyRush
"""
import os
import sys
from database import get_db, is_db_available

def test_connection():
    """Test database connection"""
    try:
        print("Testing database connection...")
        print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')}")

        # Test basic connectivity
        if is_db_available():
            print("✅ Database connection successful!")

            # Test getting a session
            db = next(get_db())
            result = db.execute("SELECT 1 as test")
            row = result.fetchone()
            db.close()

            if row and row[0] == 1:
                print("✅ Database query successful!")
                return True
            else:
                print("❌ Database query failed!")
                return False
        else:
            print("❌ Database connection failed!")
            return False

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
