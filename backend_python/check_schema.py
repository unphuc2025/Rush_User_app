from database import engine
from sqlalchemy import text

def check_table_schema():
    with engine.connect() as connection:
        print("🔍 Checking 'profiles' table columns:")
        result = connection.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'profiles'
            ORDER BY ordinal_position;
        """))
        
        columns = result.fetchall()
        for col in columns:
            print(f"   - {col[0]} ({col[1]})")

if __name__ == "__main__":
    check_table_schema()
