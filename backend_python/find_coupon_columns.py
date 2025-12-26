import sys
sys.path.append('.')
from database import engine
from sqlalchemy import text

def find_columns():
    try:
        with engine.connect() as conn:
            # Check if table exists
            table_check = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_name = 'admin_coupons'"))
            if not table_check.fetchone():
                print("❌ admin_coupons table does not exist!")
                return

            print("✅ admin_coupons table exists\n")

            # Get all columns
            col_result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'admin_coupons'
                ORDER BY ordinal_position
            """))
            columns = col_result.fetchall()

            print(f"Your admin_coupons table has {len(columns)} columns:")
            print("=" * 50)
            for i, col in enumerate(columns, 1):
                print(f"{i}. {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")

            print("\n" + "=" * 50)
            print("Please tell me which columns correspond to:")
            print("• Coupon Code (what should I use to find the coupon?)")
            print("• Discount Percentage (the % discount value)")
            print("• Start Date (when coupon becomes valid)")
            print("• End Date (when coupon expires)")
            print("• Active Status (boolean: true/false if coupon is active)")

            print("\nExample: 'coupon_code' for Coupon Code, 'discount_percent' for Discount, etc.")

            # Check if any data exists
            count_result = conn.execute(text("SELECT COUNT(*) FROM admin_coupons"))
            count = count_result.scalar()
            print(f"\nTable has {count} rows of data.")

            if count > 0:
                print("\nLet me try to show a sample row...")
                try:
                    # Try to select all columns
                    all_cols_query = text(f"SELECT * FROM admin_coupons LIMIT 1")
                    data_result = conn.execute(all_cols_query)
                    row = data_result.fetchone()
                    if row:
                        print("Sample data row:")
                        for col_name, value in zip([col[0] for col in columns], row):
                            print(f"  {col_name}: {value}")
                    else:
                        print("No sample data found.")
                except Exception as e:
                    print(f"Could not show sample data: {e}")

    except Exception as e:
        print(f"❌ Database error: {e}")
        print("Make sure your database is running and configured properly.")

if __name__ == "__main__":
    find_columns()
