"""
Test script to verify OTP endpoint works even without database
"""
import requests
import json

API_URL = "http://192.168.1.2:5000"

def test_send_otp():
    print("=" * 60)
    print("Testing OTP Send Endpoint")
    print("=" * 60)
    
    url = f"{API_URL}/auth/send-otp"
    payload = {
        "phone_number": "+919676402161"
    }
    
    print(f"\nSending POST request to: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! OTP endpoint is working!")
            data = response.json()
            if data.get("success"):
                print(f"✅ OTP Code: {data.get('otp_code')}")
                print(f"✅ Verification ID: {data.get('verification_id')}")
                return True
        else:
            print(f"\n❌ FAILED! Status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server!")
        print(f"Make sure the backend is running on {API_URL}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🔧 OTP Endpoint Test\n")
    print("This test will verify that the OTP endpoint works")
    print("even when the MySQL database is not available.\n")
    
    success = test_send_otp()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All tests passed!")
        print("\nThe OTP endpoint is now working in dev mode.")
        print("You can use OTP code: 12345 for testing.")
    else:
        print("❌ Tests failed!")
        print("\nPlease check:")
        print("1. Backend server is running (start_server.bat)")
        print(f"2. Server is accessible at {API_URL}")
    print("=" * 60)
