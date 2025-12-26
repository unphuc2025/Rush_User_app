import requests
import json

BASE_URL = "http://192.168.1.2:5000"

def test_profile_endpoints():
    print("=" * 60)
    print("Testing Profile Endpoints")
    print("=" * 60)
    
    # Test Cities
    try:
        url = f"{BASE_URL}/profile/cities"
        print(f"\nFetching cities from: {url}")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Cities: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception fetching cities: {e}")

    # Test Game Types
    try:
        url = f"{BASE_URL}/profile/game-types"
        print(f"\nFetching game types from: {url}")
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Game Types: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception fetching game types: {e}")

if __name__ == "__main__":
    test_profile_endpoints()
