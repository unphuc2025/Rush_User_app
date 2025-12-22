from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from passlib.context import CryptContext
import uuid
from datetime import timedelta, datetime
import random
from sqlalchemy import and_

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_phone(db: Session, phone_number: str):
    # Query User table directly now that it has phone_number
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        id=str(uuid.uuid4()),
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_with_phone(db: Session, phone_number: str, profile_data: dict | None = None):
    """Create a user record for a phone-based user and store profile data.

    `profile_data` may contain keys matching Profile fields and will be stored.
    """
    user_id = str(uuid.uuid4())
    # Use a very simple, short password for phone-based users
    # They login via OTP, never use password
    temp_password = "phone_user_temp"  # Short and simple
    
    db_user = models.User(
        id=user_id,
        email=f"{phone_number}@phone.myrush.app",
        password_hash=get_password_hash(temp_password),
        first_name=(profile_data.get("full_name") if profile_data and profile_data.get("full_name") else ""),
        last_name="",
        phone_number=phone_number
    )
    db.add(db_user)
    # prepare profile values
    profile_values = {
        "id": user_id,
        "phone_number": phone_number,
    }
    if profile_data:
        # only copy known profile fields
        allowed = [
            "full_name", "age", "city", "gender", "handedness", "skill_level", "sports", "playing_style"
        ]
        for k in allowed:
            if k in profile_data and profile_data[k] is not None:
                profile_values[k] = profile_data[k]

    db_profile = models.Profile(**profile_values)
    db.add(db_profile)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_profile(db: Session, user_id: str):
    return db.query(models.Profile).filter(models.Profile.id == user_id).first()

def create_or_update_profile(db: Session, profile: schemas.ProfileCreate, user_id: str):
    db_profile = get_profile(db, user_id)
    if db_profile:
        for key, value in profile.dict(exclude_unset=True).items():
            setattr(db_profile, key, value)
    else:
        db_profile = models.Profile(**profile.dict(), id=user_id)
        db.add(db_profile)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def create_booking(db: Session, booking: schemas.BookingCreate, user_id: str):
    try:
        print(f"[CRUD BOOKING] Starting booking creation for user: {user_id}")

        # Parse time from AM/PM format to 24-hour format
        import re
        time_str = str(booking.start_time).strip()
        print(f"[CRUD BOOKING] Parsing time: {time_str}")

        # If already in HH:MM format, use as is
        if re.match(r'^\d{1,2}:\d{2}$', time_str):
            start_time_str = time_str
        else:
            # Handle AM/PM format
            match = re.match(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?', time_str)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2))
                ampm = match.group(3)

                if ampm and ampm.upper() == 'PM' and hour != 12:
                    hour += 12
                elif ampm and ampm.upper() == 'AM' and hour == 12:
                    hour = 0

                start_time_str = f"{hour:02d}:{minute:02d}"
            else:
                start_time_str = "10:00"  # Default fallback

        print(f"[CRUD BOOKING] Parsed time to: {start_time_str}")

        # Calculate end_time using string time
        from datetime import datetime as dt
        start_dt = dt.strptime(start_time_str, '%H:%M').time()
        start_datetime = dt.combine(booking.booking_date, start_dt)
        end_dt = start_datetime + timedelta(minutes=booking.duration_minutes)
        end_time = end_dt.time()

        price_per_hour = booking.price_per_hour or 200.0 # Use selected price or default
        number_of_players = booking.number_of_players or 2
        total_amount = price_per_hour * (booking.duration_minutes / 60.0) * number_of_players

        print(f"[CRUD BOOKING] Calculations: price_per_hour={price_per_hour}, duration_minutes={booking.duration_minutes}, number_of_players={number_of_players}, total_amount={total_amount}")

        # Check if court exists in admin_courts table
        from sqlalchemy import text
        court_check = db.execute(
            text("SELECT id FROM admin_courts WHERE id = :court_id"),
            {"court_id": str(booking.court_id)}
        ).fetchone()
        
        if not court_check:
            print(f"[CRUD BOOKING] ERROR: Court {booking.court_id} does not exist in admin_courts")
            raise ValueError(f"Court {booking.court_id} not found in admin_courts table")
        
        print(f"[CRUD BOOKING] ✅ Court {booking.court_id} found in admin_courts")

        # Check if user exists
        user_exists = db.query(models.User).filter(models.User.id == user_id).first()
        if not user_exists:
            print(f"[CRUD BOOKING] ERROR: User {user_id} does not exist")
            raise ValueError(f"User {user_id} not found")

        # Don't set id - let PostgreSQL generate it with uuid_generate_v4()
        booking_data = {
            "user_id": user_id,
            "court_id": booking.court_id,  # Changed from venue_id to court_id
            "booking_date": booking.booking_date,
            "start_time": booking.start_time,
            "end_time": end_time,
            "duration_minutes": booking.duration_minutes,
            "number_of_players": number_of_players,
            "team_name": booking.team_name,
            "special_requests": booking.special_requests,
            "price_per_hour": price_per_hour,
            "total_amount": total_amount,
            # Mark booking as confirmed immediately on successful creation.
            # Payment can still be tracked separately via payment_status.
            "status": "confirmed",
            "payment_status": "pending"
        }

        # Adjust data types for MySQL compatibility
        adjusted_booking_data = {
            **booking_data,
            'start_time': start_dt,  # Use the parsed start TIME object
            'end_time': end_time,    # end_time is already TIME object
            'booking_date': booking.booking_date,  # Ensure date format
        }

        print(f"[CRUD BOOKING] Creating booking with adjusted data: {adjusted_booking_data}")

        db_booking = models.Booking(**adjusted_booking_data)
        db.add(db_booking)

        print("[CRUD BOOKING] Committing to database...")
        db.commit()

        print(f"[CRUD BOOKING] Refreshing booking data for ID: {db_booking.id}")
        db.refresh(db_booking)

        print(f"[CRUD BOOKING] SUCCESS: Booking created with ID: {db_booking.id}, total_amount: {db_booking.total_amount}")
        return db_booking

    except Exception as e:
        print(f"[CRUD BOOKING] ERROR: Exception during booking creation: {e}")
        import traceback
        traceback.print_exc()
        raise e

def create_otp_record(db: Session, phone_number: str, otp_code: str, expires_at: datetime):
    otp = models.OtpVerification(
        phone_number=phone_number,
        otp_code=otp_code,
        expires_at=expires_at,
        is_verified=False
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp

def verify_otp_record(db: Session, phone_number: str, otp_code: str):
    now = datetime.utcnow()
    otp = db.query(models.OtpVerification).filter(
        and_(models.OtpVerification.phone_number == phone_number,
             models.OtpVerification.otp_code == otp_code,
             models.OtpVerification.expires_at >= now,
             models.OtpVerification.is_verified == False)
    ).first()
    if not otp:
        return None
    otp.is_verified = True
    db.commit()
    db.refresh(otp)
    return otp

def get_bookings(db: Session, user_id: str):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

def get_cities(db: Session):
    return db.query(models.AdminCity).filter(models.AdminCity.is_active == True).all()

def get_game_types(db: Session):
    return db.query(models.AdminGameType).filter(models.AdminGameType.is_active == True).all()
