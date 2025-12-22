from database import engine, SQLALCHEMY_DATABASE_URL
from sqlalchemy import text
import sys

print(f"DEBUG: SQLALCHEMY_DATABASE_URL from database.py: {SQLALCHEMY_DATABASE_URL.replace(SQLALCHEMY_DATABASE_URL.split('@')[0].split('//')[1], '***') if '@' in SQLALCHEMY_DATABASE_URL else SQLALCHEMY_DATABASE_URL}")

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(f"✅ Connection successful! Version: {result.fetchone()[0]}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()
