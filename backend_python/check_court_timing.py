import os
from dotenv import load_dotenv
import psycopg2
import json

# Load environment variables
load_dotenv()

# Database connection using DATABASE_URL
database_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(database_url)

cursor = conn.cursor()

# Check the court timing data
court_id = '07eab7f5-2f94-4048-acef-9a134990e3c5'

query = """
SELECT
    id,
    name,
    price_per_hour,
    price_conditions,
    unavailability_slots,
    is_active
FROM admin_courts
WHERE id = %s
"""

cursor.execute(query, (court_id,))
result = cursor.fetchone()

if result:
    print("="*60)
    print(f"Court ID: {result[0]}")
    print(f"Court Name: {result[1]}")
    print(f"Price Per Hour: {result[2]}")
    print(f"Is Active: {result[5]}")
    print("-"*60)
    print(f"Price Conditions (PRIMARY - for timing):")
    price_conditions = result[3]
    print(f"Raw value: {price_conditions}")
    print(f"Type: {type(price_conditions)}")
    print(f"Length: {len(price_conditions) if price_conditions else 0}")
    print("-"*60)

    if price_conditions and len(price_conditions) > 0:
        print("✅ PRICE CONDITIONS DATA FOUND")
        print("Parsed as JSON:")
        try:
            price_data = price_conditions if isinstance(price_conditions, list) else json.loads(price_conditions)
            print(json.dumps(price_data, indent=2))
            if isinstance(price_data, list) and len(price_data) > 0:
                first_entry = price_data[0]
                print("-"*60)
                print(f"First pricing entry analysis:")
                print(f"  Days: {first_entry.get('days', [])}")
                print(f"  Slot From: {first_entry.get('slotFrom', 'N/A')}")
                print(f"  Slot To: {first_entry.get('slotTo', 'N/A')}")
                print(f"  Price: {first_entry.get('price', 'N/A')}")
        except Exception as e:
            print(f"❌ Error parsing price_conditions JSON: {e}")
    else:
        print("❌ NO PRICE CONDITIONS - checking unavailability_slots")

        # Check unavailability_slots as backup
        unavail_slots = result[4]
        print("-"*60)
        print(f"Unavailability Slots (BACKUP):")
        print(f"Raw value: {unavail_slots}")
        print(f"Type: {type(unavail_slots)}")
        print(f"Length: {len(unavail_slots) if unavail_slots else 0}")

        if unavail_slots and len(unavail_slots) > 0:
            print("✅ UNAVAILABILITY_SLOTS DATA FOUND")
            print("Parsed as JSON:")
            try:
                unavail_data = unavail_slots if isinstance(unavail_slots, list) else json.loads(unavail_slots)
                print(json.dumps(unavail_data, indent=2))
            except Exception as e:
                print(f"❌ Error parsing unavailability_slots JSON: {e}")
        else:
            print("❌ NO DATA IN EITHER FIELD")
    print("="*60)
else:
    print(f"Court {court_id} not found!")

cursor.close()
conn.close()
