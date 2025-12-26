#!/usr/bin/env python3
"""
Test script to verify booking creation and storage works correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import User, Venue, Booking
from crud import create_user, create_booking
from schemas import BookingCreate
from datetime import date, time
import uuid

def create_sample_data():
    """Create sample user, venue, and booking"""
    db = SessionLocal()

    try:
        print("🚀 Creating sample booking data...")

        # Check/create sample user
        sample_user_id = "550e8400-e29b-41d4-a716-446655440000"  # Proper UUID format
        user = db.query(User).filter(User.id == sample_user_id).first()
        if not user:
            print("👤 Creating sample user...")
            user = User(
                id=sample_user_id,
                email="test@example.com",
                password_hash="hashed_password",
                first_name="Test",
                last_name="User"
            )
            db.add(user)
            db.commit()

        # Check/create sample venue
        sample_venue_id = "550e8400-e29b-41d4-a716-446655440001"  # Proper UUID format
        venue = db.query(Venue).filter(Venue.id == sample_venue_id).first()
        if not venue:
            print("🏟️ Creating sample venue...")
            venue = Venue(
                id=sample_venue_id,
                court_name="Test Arena",
                location="HSR Layout, Bengaluru",
                game_type="Cricket",
                prices="200",
                description="Test cricket arena"
            )
            db.add(venue)
            db.commit()

        # Create booking data
        booking_data = BookingCreate(
            venue_id=sample_venue_id,
            booking_date=date(2025, 12, 15),  # Future date
            start_time="02:00 PM",  # Test AM/PM parsing
            duration_minutes=120,  # 2 hours
            number_of_players=3,
            price_per_hour=250.0,
            team_name="Test Team",
            special_requests="Need extra stumps"
        )

        print("📋 Booking Details:")
        print(f"   Venue ID: {sample_venue_id}")
        print(f"   Date: {booking_data.booking_date}")
        print(f"   Time: {booking_data.start_time}")
        print(f"   Duration: {booking_data.duration_minutes} mins")
        print(f"   Players: {booking_data.number_of_players}")
        print(f"   Price/Hour: ₹{booking_data.price_per_hour}")

        # Calculate expected total
        expected_total = booking_data.price_per_hour * (booking_data.duration_minutes / 60.0) * booking_data.number_of_players
        print(f"   Expected Total: ₹{expected_total}")

        # Create booking
        print("\n🎯 Creating booking...")
        result = create_booking(db, booking_data, sample_user_id)

        print("✅ SUCCESS: Booking created!")
        print(f"   Booking ID: {result.id}")
        print(f"   User ID: {result.user_id}")
        print(f"   Venue ID: {result.venue_id}")
        print(f"   Date: {result.booking_date}")
        print(f"   Start Time: {result.start_time}")
        print(f"   End Time: {result.end_time}")
        print(f"   Duration: {result.duration_minutes} mins")
        print(f"   Players: {result.number_of_players}")
        print(f"   Team: {result.team_name}")
        print(f"   Price/Hour: ₹{result.price_per_hour}")
        print(f"   Total Amount: ₹{result.total_amount}")
        print(f"   Status: {result.status}")

        # Verify data matches expected calculation
        if abs(result.total_amount - expected_total) < 0.01:
            print("✅ TOTAL CALCULATION CORRECT!")
        else:
            print(f"❌ TOTAL MISMATCH: Expected ₹{expected_total}, Got ₹{result.total_amount}")

        # Test fetching the booking back
        print("\n🔍 Testing database retrieval...")
        fetched_booking = db.query(Booking).filter(Booking.id == result.id).first()
        if fetched_booking:
            print("✅ Booking retrieved successfully from database!")
        else:
            print("❌ Failed to retrieve booking from database!")

        print(f"\n🎉 SAMPLE BOOKING CREATION TEST COMPLETED SUCCESSFULLY!")
        print(f"   Booking ID: {result.id}")
        print(f"   Total Amount: ₹{result.total_amount}")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
