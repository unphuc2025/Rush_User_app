"""
Test script to verify new user flow
"""
import requests
import json

BASE_URL = "http://192.168.1.2:5000"
NEW_PHONE = "+919999999999"  # Use a number that doesn't exist

print("="*60)
print("Testing New User Flow")
print("="*60)

# Step 1: Send OTP
print("\n1. Sending OTP...")
response = requests.post(f"{BASE_URL}/auth/send-otp", json={"phone_number": NEW_PHONE})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Step 2: Verify OTP (without profile data)
print("\n2. Verifying OTP (without profile data)...")
response = requests.post(f"{BASE_URL}/auth/verify-otp", json={
    "phone_number": NEW_PHONE,
    "otp_code": "12345"
})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.json().get("needs_profile"):
    print("\n✅ Backend correctly returns needs_profile: true")
    print("   Frontend should navigate to PlayerProfileScreen")
else:
    print("\n❌ Backend did NOT return needs_profile")
    print("   This is the issue!")

print("\n" + "="*60)
