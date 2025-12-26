from database import engine
from sqlalchemy import text
from models import AdminCourt
from sqlalchemy.orm import Session
from database import SessionLocal

def test_venues_query():
    print("Testing venues query...")
    
    # Test 1: Raw SQL query
    print("\n=== Test 1: Raw SQL Query ===")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM admin_courts WHERE is_active = true"))
            rows = result.fetchall()
            print(f"Found {len(rows)} active courts")
            for row in rows:
                print(f"  - Court: {dict(row)}")
    except Exception as e:
        print(f"Error in raw SQL: {e}")
    
    # Test 2: SQLAlchemy ORM query
    print("\n=== Test 2: SQLAlchemy ORM Query ===")
    try:
        db = SessionLocal()
        courts = db.query(AdminCourt).filter(AdminCourt.is_active == True).all()
        print(f"Found {len(courts)} courts via ORM")
        for court in courts:
            print(f"  - ID: {court.id}")
            print(f"    Name: {court.name}")
            print(f"    Branch ID: {court.branch_id}")
            print(f"    Game Type ID: {court.game_type_id}")
            print(f"    Price: {court.price_per_hour}")
        db.close()
    except Exception as e:
        print(f"Error in ORM query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_venues_query()
