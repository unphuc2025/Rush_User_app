import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def test_postgres_connection():
    """Test PostgreSQL database connection"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in .env file")
        print("\nPlease ensure your .env file contains:")
        print("DATABASE_URL=postgresql://username:password@host:port/database")
        return False
    
    print(f"🔍 Testing connection to PostgreSQL...")
    print(f"📍 Connection string: {database_url.replace(database_url.split('@')[0].split('//')[1], '***')}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Successfully connected to PostgreSQL!")
            print(f"📊 Database version: {version}")
            
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"\n📋 Found {len(tables)} table(s):")
                for table in tables:
                    print(f"   - {table}")
            else:
                print("\n⚠️  No tables found in the database")
                print("   You mentioned tables are already created - please verify.")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n💡 Common issues:")
        print("   1. Check if PostgreSQL is running")
        print("   2. Verify DATABASE_URL in .env file")
        print("   3. Ensure database exists")
        print("   4. Check username/password")
        print("   5. Verify host and port")
        return False

if __name__ == "__main__":
    test_postgres_connection()
