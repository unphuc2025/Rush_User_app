import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL", "NOT_SET")

print("Current DATABASE_URL from .env file:")
if database_url != "NOT_SET":
    # Hide password for security
    if "@" in database_url and "://" in database_url:
        protocol = database_url.split("://")[0]
        rest = database_url.split("://")[1]
        if "@" in rest:
            credentials = rest.split("@")[0]
            host_part = rest.split("@")[1]
            username = credentials.split(":")[0] if ":" in credentials else credentials
            hidden = f"{protocol}://{username}:***@{host_part}"
            print(hidden)
        else:
            print(database_url)
    else:
        print(database_url)
else:
    print("❌ DATABASE_URL is not set in .env file!")
    print("\nExpected format:")
    print("DATABASE_URL=postgresql://username:password@host:port/database")
