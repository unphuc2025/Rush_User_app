from database import engine
from sqlalchemy import text

def migrate_users_table():
    with engine.connect() as connection:
        print("🔧 Migrating 'users' table...")
        
        # List of columns to check/add to match models.py User model
        columns_to_add = [
            ("password_hash", "VARCHAR(255)"),
            ("first_name", "VARCHAR(50)"),
            ("last_name", "VARCHAR(50)")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                print(f"   Checking {col_name}...")
                connection.execute(text(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_type};"))
                print(f"   ✅ Added/Verified {col_name}")
            except Exception as e:
                print(f"   ❌ Error adding {col_name}: {e}")
                
        connection.commit()
        print("\n✨ Migration complete!")

if __name__ == "__main__":
    migrate_users_table()
