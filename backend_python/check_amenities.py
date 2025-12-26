#!/usr/bin/env python3
"""
Check amenities tables in the database
"""
import os
import sys
sys.path.append('.')

from database import get_db
from sqlalchemy import text

def check_amenities():
    """Check amenities tables"""
    try:
        db = next(get_db())

        print("=== ADMIN_AMENITIES TABLE ===")
        result = db.execute(text("SELECT * FROM admin_amenities"))
        columns = list(result.keys())
        print(f"Columns: {columns}")
        rows = result.fetchall()
        print(f"Rows: {len(rows)}")
        for row in rows:
            print(dict(row._mapping))

        print("\n=== ADMIN_BRANCH_AMENITIES TABLE ===")
        result = db.execute(text("SELECT * FROM admin_branch_amenities"))
        columns = list(result.keys())
        print(f"Columns: {columns}")
        rows = result.fetchall()
        print(f"Rows: {len(rows)}")
        for row in rows:
            print(dict(row._mapping))

        db.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_amenities()
