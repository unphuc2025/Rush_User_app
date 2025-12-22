from database import engine
from sqlalchemy import text

def migrate_profiles_table():
    with engine.connect() as connection:
        print("🔧 Migrating 'profiles' table...")
        
        # List of columns to check/add
        columns_to_add = [
            ("phone_number", "VARCHAR(20)"),
            ("full_name", "VARCHAR(100)"),
            ("age", "INTEGER"),
            ("city", "VARCHAR(100)"),
            ("gender", "VARCHAR(20)"),
            ("handedness", "VARCHAR(20)"),
            ("skill_level", "VARCHAR(50)"),
            ("sports", "JSONB"),  # Use JSONB for Postgres
            ("playing_style", "VARCHAR(100)")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                print(f"   Checking {col_name}...")
                connection.execute(text(f"ALTER TABLE profiles ADD COLUMN IF NOT EXISTS {col_name} {col_type};"))
                print(f"   ✅ Added/Verified {col_name}")
            except Exception as e:
                print(f"   ❌ Error adding {col_name}: {e}")
                
        connection.commit()
        print("\n✨ Migration complete!")

if __name__ == "__main__":
    migrate_profiles_table()
