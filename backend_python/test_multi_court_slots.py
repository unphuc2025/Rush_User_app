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

def test_multi_court_slots():
    """Test slot generation across multiple courts and cities"""

    courts_data = [
        {
            "id": "07eab7f5-2f94-4048-acef-9a134990e3c5",  # Bengaluru court
            "name": "Bengaluru Court",
            "city": "Bengaluru",
            "price_conditions": [
                {
                    "id": 1765366374948,
                    "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                    "price": "200",
                    "slotTo": "06:00",
                    "slotFrom": "05:00"
                },
                {
                    "id": 1765376886021,
                    "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                    "price": "400",
                    "slotTo": "07:00",
                    "slotFrom": "06:00"
                }
            ],
            "expected_slots_monday": [
                {"time": "05:00", "price": 200.0},
                {"time": "06:00", "price": 400.0}
            ]
        },
        {
            "id": "sample-court-hyderabad",  # Hyderabad court
            "name": "Hyderabad Court",
            "city": "Hyderabad",
            "price_conditions": [
                {
                    "id": 1234567890,
                    "days": ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
                    "price": "150",
                    "slotTo": "12:00",
                    "slotFrom": "08:00"
                }
            ],
            "expected_slots_monday": [
                {"time": "08:00", "price": 150.0},
                {"time": "09:00", "price": 150.0},
                {"time": "10:00", "price": 150.0},
                {"time": "11:00", "price": 150.0}
            ]
        },
        {
            "id": "sample-court-delhi",  # Delhi court
            "name": "Delhi Court",
            "city": "Delhi",
            "price_conditions": [
                {
                    "id": 9876543210,
                    "days": ["wed", "fri", "sat"],
                    "price": "300",
                    "slotTo": "20:00",
                    "slotFrom": "18:00"
                }
            ],
            "expected_slots_friday": [
                {"time": "18:00", "price": 300.0},
                {"time": "19:00", "price": 300.0}
            ]
        }
    ]

    # Update each court's price_conditions
    update_query = """
    UPDATE admin_courts
    SET price_conditions = %s
    WHERE id = %s
    """

    for court in courts_data:
        price_json = json.dumps(court["price_conditions"])
        cursor.execute(update_query, (price_json, court["id"]))
        print(f"✅ Updated {court['name']} with timing data")

    conn.commit()

    # Test each court
    test_query = """
    SELECT ac.id, ac.name, ac.price_conditions
    FROM admin_courts ac
    WHERE ac.id IN %s
    """

    court_ids = tuple(court["id"] for court in courts_data)
    cursor.execute(test_query, (court_ids,))

    results = cursor.fetchall()

    print("\n" + "="*80)
    print("🧪 MULTI-COURT SLOT GENERATION TEST RESULTS")
    print("="*80)

    for result in results:
        court_id, court_name, price_conditions = result
        
        # Find court data
        court_info = next(c for c in courts_data if c["id"] == court_id)
        
        print(f"\n🏟️ COURT: {court_name} ({court_info['city']})")
        print(f"📍 Court ID: {court_id}")
        
        if price_conditions:
            data = price_conditions
            print(f"📊 Price Conditions Configs: {len(data)}")
            
            for i, config in enumerate(data, 1):
                days = config.get("days", [])
                price = config.get("price", "N/A")
                slot_from = config.get("slotFrom", "N/A")
                slot_to = config.get("slotTo", "N/A")
                
                hours_range = f"{slot_from}-{slot_to}" if slot_from != "N/A" and slot_to != "N/A" else "N/A"
                expected_slots = int(slot_to.split(":")[0]) - int(slot_from.split(":")[0]) if slot_from != "N/A" and slot_to != "N/A" else 0
                
                print(f"   📋 Config {i}: {hours_range}, ₹{price}, {len(days)} days → {expected_slots} slots")
                
                if days:
                    print(f"      🗓️ Days: {', '.join(days[:3])}{'...' if len(days) > 3 else ''}")
        else:
            print("❌ No price conditions configured")
            
        print(f"   ✅ Expected: Varies by day (Monday/Friday specific)")

    print("\n" + "="*80)
    print("🎯 API TEST: Check each court on Monday vs Friday")
    print("="*80)
    print("   🏟️ Bengaluru Court (Monday): Should show 2 slots")
    print("      - 05:00 AM - ₹200")
    print("      - 06:00 AM - ₹400")
    print()
    print("   🏟️ Hyderabad Court (Monday): Should show 4 slots") 
    print("      - 08:00 AM-11:00 AM, all ₹150")
    print()
    print("   🏟️ Delhi Court (Friday): Should show 2 slots")
    print("      - 06:00 PM-07:00 PM, all ₹300")
    print()
    print("   🏟️ Delhi Court (Monday): Should show 0 slots (no weekend)")
    print("="*80)
    print("🎉 All courts configured for price_conditions slot generation!")
    print("="*80)

if __name__ == "__main__":
    try:
        test_multi_court_slots()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
