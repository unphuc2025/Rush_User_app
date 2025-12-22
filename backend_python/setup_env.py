"""
Interactive script to set up .env file with Supabase credentials
"""

import os

print("=" * 60)
print("MyRush Backend - Environment Setup")
print("=" * 60)
print()

# Check if .env already exists
if os.path.exists('.env'):
    print("⚠️  .env file already exists!")
    response = input("Do you want to overwrite it? (y/n): ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        exit()

print("\nPlease provide your Supabase database credentials:")
print("(You can find these in your Supabase project settings)")
print()

# Get Supabase password
print("Your Supabase host: db.vqglejkydwtopmllymuf.supabase.co")
password = input("Enter your Supabase database password: ")

if not password:
    print("❌ Password cannot be empty!")
    exit()

# Create .env content
env_content = f"""# Database Configuration
# Supabase PostgreSQL Database
DATABASE_URL=postgresql://postgres:{password}@db.vqglejkydwtopmllymuf.supabase.co:5432/postgres?sslmode=require

# JWT Configuration
SECRET_KEY=myrush_secret_key_change_this_in_production_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""

# Write to .env file
with open('.env', 'w') as f:
    f.write(env_content)

print()
print("=" * 60)
print("✅ .env file created successfully!")
print("=" * 60)
print()
print("Your configuration:")
print(f"  Database: PostgreSQL (Supabase)")
print(f"  Host: db.vqglejkydwtopmllymuf.supabase.co")
print(f"  Database: postgres")
print(f"  SSL: Required")
print()
print("Next steps:")
print("  1. Start the backend: python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload")
print("  2. Test the connection: python test_profile_endpoints.py")
print()

