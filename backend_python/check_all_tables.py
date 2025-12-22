from database import engine
from sqlalchemy import text

def check_all_tables():
    print("=" * 80)
    print("CHECKING ALL TABLES IN POSTGRESQL DATABASE")
    print("=" * 80)
    
    try:
        with engine.connect() as connection:
            # Get all tables
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = result.fetchall()
            print(f"\n✅ Found {len(tables)} tables in database:\n")
            
            for table in tables:
                table_name = table[0]
                print(f"\n{'='*80}")
                print(f"TABLE: {table_name}")
                print(f"{'='*80}")
                
                # Get column details
                col_result = connection.execute(text(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position;
                """))
                
                columns = col_result.fetchall()
                print(f"\nColumns ({len(columns)}):")
                for col in columns:
                    nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                    default = f" DEFAULT {col[3]}" if col[3] else ""
                    print(f"  • {col[0]:<30} {col[1]:<20} {nullable}{default}")
                
                # Get row count
                count_result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = count_result.scalar()
                print(f"\n📊 Total Rows: {count}")
                
                # Show sample data if table has rows
                if count > 0 and count <= 5:
                    print(f"\n📋 Sample Data (all {count} rows):")
                    sample_result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
                    sample_rows = sample_result.fetchall()
                    
                    for i, row in enumerate(sample_rows, 1):
                        print(f"\n  Row {i}:")
                        row_dict = dict(row._mapping)
                        for key, value in row_dict.items():
                            # Truncate long values
                            str_value = str(value)
                            if len(str_value) > 100:
                                str_value = str_value[:100] + "..."
                            print(f"    {key}: {str_value}")
                elif count > 5:
                    print(f"\n📋 Sample Data (first 3 rows):")
                    sample_result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 3"))
                    sample_rows = sample_result.fetchall()
                    
                    for i, row in enumerate(sample_rows, 1):
                        print(f"\n  Row {i}:")
                        row_dict = dict(row._mapping)
                        for key, value in row_dict.items():
                            str_value = str(value)
                            if len(str_value) > 100:
                                str_value = str_value[:100] + "..."
                            print(f"    {key}: {str_value}")
            
            print(f"\n{'='*80}")
            print("✅ DATABASE CHECK COMPLETE")
            print(f"{'='*80}\n")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_all_tables()
