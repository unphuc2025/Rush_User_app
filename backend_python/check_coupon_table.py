import sys
sys.path.append('.')
from database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        # Check if table exists
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_name = 'admin_coupons'"))
        if result.fetchone():
            print("admin_coupons table exists")

            # Get columns
            col_result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'admin_coupons'
                ORDER BY ordinal_position
            """))
            columns = col_result.fetchall()
            print(f"Columns ({len(columns)}):")
            for col in columns:
                default_val = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}{default_val}")

            # Check if any data exists
            count_result = conn.execute(text("SELECT COUNT(*) FROM admin_coupons"))
            count = count_result.scalar()
            print(f"Rows: {count}")

            if count > 0:
                # Show sample data
                data_result = conn.execute(text("SELECT code, discount, start_date, end_date, active FROM admin_coupons LIMIT 3"))
                rows = data_result.fetchall()
                print("Sample data:")
                for row in rows:
                    print(f"  Code: {row[0]}, Discount: {row[1]}%, Active: {row[4]}, Valid: {row[2]} to {row[3]}")
        else:
            print("admin_coupons table does not exist - run create_coupons_table.py to create it")

except Exception as e:
    print(f"Database error: {e}")
    print("Make sure your database is running and configured properly.")
