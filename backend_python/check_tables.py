from database import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in database:", tables)

if 'otp_verifications' in tables:
    print("\n✓ otp_verifications table exists")
    columns = inspector.get_columns('otp_verifications')
    print("Columns:")
    for col in columns:
        print(f"  - {col['name']}: {col['type']}")
else:
    print("\n✗ otp_verifications table DOES NOT exist")
    print("This is likely the cause of the 500 error!")
