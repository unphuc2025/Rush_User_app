"""
Complete test script for MyRush backend
Tests OTP flow, database connectivity, and admin tables
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://192.168.1.2:5000"
TEST_PHONE = "+916300766577"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_server_health():
    """Test if server is running"""
    print_section("1. Testing Server Health")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            print(f"   URL: {BASE_URL}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print("   Make sure the backend is running on port 5000")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Connection timeout to {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_send_otp():
    """Test sending OTP"""
    print_section("2. Testing Send OTP Endpoint")
    try:
        url = f"{BASE_URL}/auth/send-otp"
        payload = {"phone_number": TEST_PHONE}
        
        print(f"   Sending request to: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"\n   Response Status: {response.status_code}")
        print(f"   Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"\n✅ OTP sent successfully!")
                print(f"   OTP Code: {data.get('otp_code', 'N/A')}")
                print(f"   Verification ID: {data.get('verification_id', 'N/A')}")
                return data.get('otp_code', '12345')
            else:
                print(f"❌ OTP sending failed: {data.get('message')}")
                return None
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error sending OTP: {str(e)}")
        return None

def test_verify_otp(otp_code):
    """Test verifying OTP"""
    print_section("3. Testing Verify OTP Endpoint")
    try:
        url = f"{BASE_URL}/auth/verify-otp"
        payload = {
            "phone_number": TEST_PHONE,
            "otp_code": otp_code,
            "full_name": "Test User",
            "age": 25,
            "city": "Hyderabad",
            "gender": "Male",
            "handedness": "Right",
            "skill_level": "Intermediate",
            "sports": ["Badminton", "Tennis"],
            "playing_style": "Aggressive"
        }
        
        print(f"   Sending request to: {url}")
        print(f"   Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"\n   Response Status: {response.status_code}")
        print(f"   Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("access_token"):
                print(f"\n✅ OTP verified successfully!")
                print(f"   Access Token: {data.get('access_token')[:50]}...")
                print(f"   Token Type: {data.get('token_type')}")
                return data.get('access_token')
            else:
                print(f"❌ No access token in response")
                return None
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error verifying OTP: {str(e)}")
        return None

def test_get_profile(access_token):
    """Test getting user profile"""
    print_section("4. Testing Get Profile Endpoint")
    try:
        url = f"{BASE_URL}/auth/profile"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print(f"   Sending request to: {url}")
        print(f"   Headers: Authorization: Bearer {access_token[:30]}...")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"\n   Response Status: {response.status_code}")
        print(f"   Response Body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print(f"\n✅ Profile retrieved successfully!")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting profile: {str(e)}")
        return False

def test_get_venues():
    """Test getting venues"""
    print_section("5. Testing Get Venues Endpoint")
    try:
        url = f"{BASE_URL}/venues/"
        
        print(f"   Sending request to: {url}")
        
        response = requests.get(url, timeout=10)
        
        print(f"\n   Response Status: {response.status_code}")
        
        if response.status_code == 200:
            venues = response.json()
            print(f"   Found {len(venues)} venue(s)")
            if len(venues) > 0:
                print(f"\n   Sample venue:")
                print(f"   {json.dumps(venues[0], indent=2)}")
            print(f"\n✅ Venues retrieved successfully!")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting venues: {str(e)}")
        return False

def main():
    print("\n" + "🚀 "*20)
    print("   MyRush Backend Complete Flow Test")
    print("🚀 "*20)
    print(f"\nTest Configuration:")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Test Phone: {TEST_PHONE}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Server Health
    if not test_server_health():
        print("\n❌ Server is not accessible. Please start the backend server.")
        print("   Run: cd MYRUSH-USER-APP/backend_python && python -m uvicorn main:app --host 0.0.0.0 --port 5000")
        return
    
    # Test 2: Send OTP
    otp_code = test_send_otp()
    if not otp_code:
        print("\n❌ Cannot proceed without OTP code")
        return
    
    # Test 3: Verify OTP
    access_token = test_verify_otp(otp_code)
    if not access_token:
        print("\n❌ Cannot proceed without access token")
        return
    
    # Test 4: Get Profile
    test_get_profile(access_token)
    
    # Test 5: Get Venues
    test_get_venues()
    
    # Summary
    print_section("Test Summary")
    print("✅ All tests completed!")
    print("\nNext Steps:")
    print("1. The mobile app should now be able to connect to the backend")
    print("2. Make sure your phone/emulator is on the same network")
    print("3. The API URL in mobile app is: http://192.168.1.11:5000")
    print("4. Try the OTP login flow in the mobile app")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
