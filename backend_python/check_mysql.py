from database import engine
from sqlalchemy import text

def check_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            db_name = result.scalar()
            print(f"✅ Successfully connected to database: {db_name}")
            
            # Check tables
            result = connection.execute(text("SHOW TABLES;"))
            tables = [row[0] for row in result]
            print(f"📊 Tables found: {tables}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_connection()
