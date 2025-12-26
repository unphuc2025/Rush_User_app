from database import engine
from sqlalchemy import text
import sys

def check_users_schema():
    try:
        with engine.connect() as connection:
            print("Checking users table columns...", flush=True)
            result = connection.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            print(f"Found {len(columns)} columns:", flush=True)
            for col in columns:
                print(f"   - {col[0]} ({col[1]})", flush=True)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_users_schema()
