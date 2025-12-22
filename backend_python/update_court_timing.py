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

# Court ID to update
court_id = '07eab7f5-2f94-4048-acef-9a134990e3c5'

# Timing data to insert - Multiple slots configuration
timing_data = [
    {
        "id": 1765366374948,
        "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        "price": "200",
        "slotTo": "06:00",
        "slotFrom": "05:00"
    },
    {
        "id": 1765366374949,
        "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        "price": "250",
        "slotTo": "10:00",
        "slotFrom": "08:00"
    },
    {
        "id": 1765366374950,
        "days": ["fri", "sat", "sun"],
        "price": "300",
        "slotTo": "16:00",
        "slotFrom": "14:00"
    }
]

# Convert to JSON string
timing_json = json.dumps(timing_data)

# Update the court with timing data
update_query = """
UPDATE admin_courts
SET unavailability_slots = %s
WHERE id = %s
"""

try:
    # First, let's see what's currently in the database
    check_query = "SELECT unavailability_slots FROM admin_courts WHERE id = %s"
    cursor.execute(check_query, (court_id,))
    current_data = cursor.fetchone()

    print("="*60)
    print(f"BEFORE UPDATE - Court: {court_id}")
    print(f"Current unavailability_slots: {current_data[0] if current_data else 'NOT FOUND'}")
    print("="*60)

    # Try the update with JSON string
    cursor.execute(update_query, (timing_json, court_id))  # Pass as JSON string
    conn.commit()

    print("✅ UPDATE EXECUTED")

    # Verify the update
    verify_query = "SELECT unavailability_slots FROM admin_courts WHERE id = %s"
    cursor.execute(verify_query, (court_id,))
    result = cursor.fetchone()

    print("="*60)
    print("AFTER UPDATE VERIFICATION:")
    if result and result[0]:
        saved_data = result[0]
        print("✓ Data found in database!")
        print(f"Saved data type: {type(saved_data)}")
        print(f"Saved data length: {len(saved_data) if saved_data else 0}")
        print(f"Raw saved data: {saved_data}")

        if isinstance(saved_data, list) and len(saved_data) > 0:
            print("✓ Data structure looks correct!")
            print("Parsed data:")
            print(json.dumps(saved_data, indent=2))
        else:
            print("⚠️ Data might not be correct format")

    else:
        print("❌ No data found after update!")

    print("="*60)

except Exception as e:
    print(f"❌ Error updating court timing: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

cursor.close()
conn.close()
