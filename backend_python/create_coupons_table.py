from database import engine
from sqlalchemy import Column, String, Float, Boolean, DateTime, MetaData, Table
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

metadata = MetaData()

# Define the admin_coupons table
admin_coupons = Table('admin_coupons', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('code', String, nullable=False, unique=True),
    Column('discount', Float, nullable=False),
    Column('start_date', DateTime, nullable=False),
    Column('end_date', DateTime, nullable=False),
    Column('active', Boolean, default=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('updated_at', DateTime, default=datetime.utcnow)
)

# Create the table
try:
    metadata.create_all(engine, tables=[admin_coupons])
    print('admin_coupons table created successfully')

    # Insert some sample data
    with engine.connect() as conn:
        from sqlalchemy import text
        # Insert sample coupons
        conn.execute(text("""
            INSERT INTO admin_coupons (code, discount, start_date, end_date, active)
            VALUES
            ('WELCOME10', 10.0, '2024-01-01', '2025-12-31', true),
            ('SAVE20', 20.0, '2024-01-01', '2025-12-31', true),
            ('FLASH50', 50.0, '2024-12-12', '2024-12-13', true)
        """))
        conn.commit()
        print('Sample coupons inserted')

except Exception as e:
    print(f'Error: {e}')
