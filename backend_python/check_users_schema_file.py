from database import engine
from sqlalchemy import text
import sys

def check_users_schema():
    with open("schema_output.txt", "w") as f:
        try:
            with engine.connect() as connection:
                f.write("Checking users table columns...\n")
                result = connection.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'users'
                    ORDER BY ordinal_position;
                """))
                
                columns = result.fetchall()
                f.write(f"Found {len(columns)} columns:\n")
                for col in columns:
                    f.write(f"   - {col[0]} ({col[1]})\n")
        except Exception as e:
            f.write(f"Error: {e}\n")

if __name__ == "__main__":
    check_users_schema()
