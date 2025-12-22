from database import engine
from sqlalchemy import text

def check_admin_tables():
    print("Starting database check...")
    with open("admin_tables_schema.txt", "w") as f:
        f.write("SCRIPT STARTED\n")
        try:
            with engine.connect() as connection:
                f.write("DATABASE CONNECTED\n")

                # Check specific admin tables
                admin_tables = ['admin_cities', 'admin_game_types', 'admin_courts', 'adminvenues']
                f.write("=== CHECKING ADMIN TABLES ===\n")
                for table in admin_tables:
                    f.write(f"Checking {table}...\n")
                    try:
                        # Check if table exists
                        exists_result = connection.execute(text(f"""
                            SELECT EXISTS (
                                SELECT 1
                                FROM information_schema.tables
                                WHERE table_schema = 'public'
                                AND table_name = '{table}'
                            );
                        """))
                        exists = exists_result.scalar()

                        if exists:
                            f.write(f"   [EXISTS] Table {table} EXISTS\n")

                            # Get column details
                            result = connection.execute(text(f"""
                                SELECT column_name, data_type, is_nullable, column_default
                                FROM information_schema.columns
                                WHERE table_name = '{table}'
                                ORDER BY ordinal_position;
                            """))

                            columns = result.fetchall()
                            f.write(f"   Columns ({len(columns)}):\n")
                            for col in columns:
                                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                                default = f" DEFAULT {col[3]}" if col[3] else ""
                                f.write(f"     - {col[0]} ({col[1]}) {nullable}{default}\n")

                            # Get row count
                            count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                            count = count_result.scalar()
                            f.write(f"   Rows: {count}\n")

                            # Show sample data if table has rows
                            if count > 0:
                                f.write("   Sample data:\n")
                                try:
                                    sample_result = connection.execute(text(f"SELECT * FROM {table} LIMIT 2"))
                                    sample_rows = sample_result.fetchall()
                                    for i, row in enumerate(sample_rows):
                                        f.write(f"     Row {i+1}: {dict(row)}\n")
                                except Exception as sample_error:
                                    f.write(f"     Error getting sample data: {sample_error}\n")
                        else:
                            f.write(f"   [NOT FOUND] Table {table} does NOT exist\n")

                    except Exception as table_error:
                        f.write(f"   [ERROR] Error checking {table}: {table_error}\n")

                    f.write("\n")

        except Exception as e:
            f.write(f"[DB ERROR] DATABASE CONNECTION ERROR: {e}\n")
            f.write("This could mean:\n")
            f.write("1. Database server is not running\n")
            f.write("2. Connection credentials are wrong\n")
            f.write("3. Network connectivity issues\n")

if __name__ == "__main__":
    check_admin_tables()
