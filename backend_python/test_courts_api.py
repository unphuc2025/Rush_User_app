from database import engine
from sqlalchemy import text

def test_courts_query():
    print("=" * 80)
    print("TESTING COURTS API QUERY")
    print("=" * 80)
    
    try:
        with engine.connect() as connection:
            # Test the exact query used in courts API
            query_sql = """
                SELECT 
                    ac.id,
                    ac.name as court_name,
                    ac.price_per_hour as prices,
                    ac.images as photos,
                    ac.videos,
                    ac.created_at,
                    ac.updated_at,
                    ab.name as branch_name,
                    ab.address_line1 as location,
                    ab.search_location as description,
                    acity.name as city_name,
                    agt.name as game_type
                FROM admin_courts ac
                JOIN admin_branches ab ON ac.branch_id = ab.id
                JOIN admin_cities acity ON ab.city_id = acity.id
                JOIN admin_game_types agt ON ac.game_type_id = agt.id
                WHERE ac.is_active = true
            """
            
            print("\n1. Testing WITHOUT city filter:")
            result = connection.execute(text(query_sql))
            courts = result.fetchall()
            print(f"   Found {len(courts)} courts")
            for court in courts:
                court_dict = dict(court._mapping)
                print(f"   - {court_dict['court_name']} in {court_dict['city_name']}")
            
            print("\n2. Testing WITH city filter (Hyderabad):")
            query_with_city = query_sql + " AND LOWER(acity.name) = LOWER(:city)"
            result = connection.execute(text(query_with_city), {"city": "Hyderabad"})
            courts = result.fetchall()
            print(f"   Found {len(courts)} courts")
            for court in courts:
                court_dict = dict(court._mapping)
                print(f"   - {court_dict['court_name']} in {court_dict['city_name']}")
            
            print("\n3. Testing WITH city filter (Hyderabad with trailing space):")
            result = connection.execute(text(query_with_city), {"city": "Hyderabad "})
            courts = result.fetchall()
            print(f"   Found {len(courts)} courts")
            for court in courts:
                court_dict = dict(court._mapping)
                print(f"   - {court_dict['court_name']} in {court_dict['city_name']}")
            
            print("\n4. Checking all cities in database:")
            city_result = connection.execute(text("SELECT name FROM admin_cities"))
            cities = city_result.fetchall()
            print(f"   Available cities:")
            for city in cities:
                print(f"   - '{city[0]}'")
            
            print("\n" + "=" * 80)
            print("TEST COMPLETE")
            print("=" * 80)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_courts_query()
