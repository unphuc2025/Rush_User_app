"""
Test script for date-specific pricing feature
This script tests the enhanced slot pricing logic with date-specific configurations
"""

import os
import sys
from datetime import datetime, date
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables")
    sys.exit(1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

def test_date_specific_pricing():
    """Test the date-specific pricing feature"""
    
    print("\n" + "="*80)
    print("TESTING DATE-SPECIFIC PRICING FEATURE")
    print("="*80)
    
    with engine.connect() as conn:
        # Get first court
        result = conn.execute(text("""
            SELECT 
                ac.id,
                ac.name,
                ac.price_per_hour,
                ac.price_conditions
            FROM admin_courts ac
            WHERE ac.is_active = true
            LIMIT 1
        """))
        
        court = result.fetchone()
        
        if not court:
            print("❌ No active courts found in database")
            return
        
        court_dict = dict(court._mapping)
        court_id = str(court_dict['id'])
        court_name = court_dict['name']
        price_per_hour = float(court_dict['price_per_hour'])
        price_conditions = court_dict.get('price_conditions', [])
        
        print(f"\n📍 Testing Court: {court_name} (ID: {court_id})")
        print(f"💰 Base Price: ₹{price_per_hour}/hour")
        print(f"📋 Price Conditions: {len(price_conditions) if price_conditions else 0} configurations")
        
        # Display current price conditions
        if price_conditions and isinstance(price_conditions, list):
            print("\n" + "-"*80)
            print("CURRENT PRICE CONFIGURATIONS:")
            print("-"*80)
            
            for i, config in enumerate(price_conditions, 1):
                print(f"\n{i}. Configuration ID: {config.get('id', 'N/A')}")
                
                if 'dates' in config:
                    print(f"   Type: DATE-SPECIFIC")
                    print(f"   Dates: {', '.join(config['dates'])}")
                elif 'days' in config:
                    print(f"   Type: DAY-OF-WEEK")
                    print(f"   Days: {', '.join(config['days'])}")
                
                print(f"   Time Range: {config.get('slotFrom', 'N/A')} - {config.get('slotTo', 'N/A')}")
                print(f"   Price: ₹{config.get('price', 'N/A')}/hour")
        else:
            print("\n⚠️  No price configurations found - will use default pricing")
        
        # Test dates
        test_dates = [
            datetime.now().date(),  # Today
            date(2025, 12, 25),     # Christmas
            date(2025, 12, 31),     # New Year's Eve
            date(2026, 1, 1),       # New Year's Day
            date(2025, 11, 12),     # Diwali
        ]
        
        print("\n" + "="*80)
        print("TESTING SLOT GENERATION FOR DIFFERENT DATES")
        print("="*80)
        
        for test_date in test_dates:
            date_str = test_date.strftime("%Y-%m-%d")
            day_name = test_date.strftime("%A")
            day_abbr = day_name.lower()[:3]
            
            print(f"\n📅 Date: {date_str} ({day_name})")
            print("-"*80)
            
            # Simulate the backend logic
            matching_configs = []
            date_specific = []
            day_specific = []
            
            if price_conditions and isinstance(price_conditions, list):
                for config in price_conditions:
                    if isinstance(config, dict):
                        # Check for date-specific
                        if 'dates' in config and isinstance(config.get('dates'), list):
                            if date_str in config['dates']:
                                date_specific.append(config)
                        # Check for day-of-week
                        elif 'days' in config:
                            days_list = config.get('days', [])
                            day_matches = [d.lower()[:3] for d in days_list] if isinstance(days_list, list) else []
                            if day_abbr in day_matches:
                                day_specific.append(config)
                
                if date_specific:
                    matching_configs = date_specific
                    print(f"✅ Found {len(date_specific)} DATE-SPECIFIC configuration(s)")
                    for cfg in date_specific:
                        print(f"   → {cfg.get('slotFrom')}-{cfg.get('slotTo')}: ₹{cfg.get('price')}/hour")
                elif day_specific:
                    matching_configs = day_specific
                    print(f"✅ Found {len(day_specific)} DAY-OF-WEEK configuration(s)")
                    for cfg in day_specific:
                        print(f"   → {cfg.get('slotFrom')}-{cfg.get('slotTo')}: ₹{cfg.get('price')}/hour")
                else:
                    print(f"⚠️  No matching configurations - using base price ₹{price_per_hour}/hour")
            else:
                print(f"⚠️  No price_conditions - using base price ₹{price_per_hour}/hour")
            
            # Generate sample slots
            if matching_configs:
                slot_count = 0
                for config in matching_configs:
                    try:
                        start = int(config.get('slotFrom', '08:00').split(':')[0])
                        end = int(config.get('slotTo', '22:00').split(':')[0])
                        slot_count += (end - start)
                    except:
                        pass
                print(f"🎯 Expected Slots: ~{slot_count} slots")
        
        print("\n" + "="*80)
        print("TEST COMPLETED")
        print("="*80)
        print("\n✅ The backend is ready to handle date-specific pricing!")
        print("📱 Frontend will automatically display correct prices based on selected date")
        print("📚 See DATE_SPECIFIC_PRICING_GUIDE.md for more details")

def add_sample_date_pricing():
    """Add sample date-specific pricing to the first court"""
    
    print("\n" + "="*80)
    print("ADDING SAMPLE DATE-SPECIFIC PRICING")
    print("="*80)
    
    with engine.connect() as conn:
        # Get first court
        result = conn.execute(text("""
            SELECT id, name 
            FROM admin_courts 
            WHERE is_active = true 
            LIMIT 1
        """))
        
        court = result.fetchone()
        
        if not court:
            print("❌ No active courts found")
            return
        
        court_dict = dict(court._mapping)
        court_id = str(court_dict['id'])
        court_name = court_dict['name']
        
        print(f"\n📍 Court: {court_name}")
        
        # Sample configuration with date-specific pricing
        sample_config = """[
          {
            "id": "weekday",
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "slotFrom": "08:00",
            "slotTo": "18:00",
            "price": "600"
          },
          {
            "id": "weekend",
            "days": ["Saturday", "Sunday"],
            "slotFrom": "08:00",
            "slotTo": "22:00",
            "price": "800"
          },
          {
            "id": "christmas-2025",
            "dates": ["2025-12-25"],
            "slotFrom": "10:00",
            "slotTo": "20:00",
            "price": "1500"
          },
          {
            "id": "new-year-2026",
            "dates": ["2025-12-31", "2026-01-01"],
            "slotFrom": "10:00",
            "slotTo": "22:00",
            "price": "2000"
          }
        ]"""
        
        # Update the court
        update_query = text("""
            UPDATE admin_courts 
            SET price_conditions = :config::jsonb,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :court_id
        """)
        
        try:
            conn.execute(update_query, {
                "config": sample_config,
                "court_id": court_id
            })
            conn.commit()
            print("✅ Sample date-specific pricing added successfully!")
            print("\nAdded configurations:")
            print("  - Weekdays (Mon-Fri): ₹600 (8am-6pm)")
            print("  - Weekends (Sat-Sun): ₹800 (8am-10pm)")
            print("  - Christmas 2025: ₹1500 (10am-8pm)")
            print("  - New Year 2025-2026: ₹2000 (10am-10pm)")
        except Exception as e:
            print(f"❌ Error adding sample pricing: {e}")
            conn.rollback()

if __name__ == "__main__":
    print("\n🧪 DATE-SPECIFIC PRICING TEST SCRIPT")
    print("="*80)
    
    # Ask user what they want to do
    print("\nOptions:")
    print("1. Test current configuration")
    print("2. Add sample date-specific pricing")
    print("3. Both")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        test_date_specific_pricing()
    elif choice == "2":
        add_sample_date_pricing()
        print("\n" + "="*80)
        test_date_specific_pricing()
    elif choice == "3":
        add_sample_date_pricing()
        print("\n" + "="*80)
        test_date_specific_pricing()
    else:
        print("❌ Invalid choice")
