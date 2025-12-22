#!/usr/bin/env python3
"""Quick script to reproduce the /bookings/ POST used by the mobile app."""
import os
import sys
import json
from datetime import datetime

import requests

BASE_URL = os.environ.get("MYRUSH_API_BASE", "http://192.168.1.2:5000")
TEST_PHONE = "+916300766577"


def main():
    print("Base URL:", BASE_URL)
    print("Test phone:", TEST_PHONE)

    # 1) Send OTP
    print("\n1) /auth/send-otp ...")
    r1 = requests.post(
        f"{BASE_URL}/auth/send-otp",
        json={"phone_number": TEST_PHONE},
        timeout=10,
    )
    print("Status:", r1.status_code)
    print("Body:", r1.text)

    # 2) Verify OTP 12345
    print("\n2) /auth/verify-otp ...")
    verify_payload = {"phone_number": TEST_PHONE, "otp_code": "12345"}
    r2 = requests.post(
        f"{BASE_URL}/auth/verify-otp",
        json=verify_payload,
        timeout=10,
    )
    print("Status:", r2.status_code)
    print("Body:", r2.text)

    try:
        token = r2.json().get("access_token")
    except Exception as e:
        print("ERROR parsing verify-otp JSON:", e)
        sys.exit(1)

    if not token:
        print("No access_token returned; cannot continue")
        sys.exit(1)

    print("Access token (first 40 chars):", token[:40] + "...")
    headers = {"Authorization": f"Bearer {token}"}

    # 3) Create booking using the **same snake_case payload** that
    # `bookingsApi.createBooking` in the mobile app sends.
    print("\n3) POST /bookings/ ...")
    booking_payload = {
        "court_id": "72ee05b1-d833-4c2c-af4c-4f20693647f5",
        "booking_date": "2025-11-24",
        "start_time": "05:00 AM",
        "duration_minutes": 60,
        "number_of_players": 3,
        "price_per_hour": 200,
        "team_name": "",
        "special_requests": "",
    }
    print("Request JSON:")
    print(json.dumps(booking_payload, indent=2))

    r3 = requests.post(
        f"{BASE_URL}/bookings/",
        json=booking_payload,
        headers=headers,
        timeout=20,
    )
    print("Status:", r3.status_code)
    print("Body:", r3.text)


if __name__ == "__main__":
    main()

