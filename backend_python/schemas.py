from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Response model for /auth/profile and other user reads.

    For phone-only login users, email/first_name/last_name may legitimately
    be missing, so we allow them to be null/omitted here.
    """

    id: UUID
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Profile Schemas
class ProfileBase(BaseModel):
    phone_number: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    handedness: Optional[str] = None
    skill_level: Optional[str] = None
    sports: Optional[List[str]] = None
    playing_style: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Venue Schemas
class VenueBase(BaseModel):
    court_name: str
    location: str
    city: Optional[str] = None
    game_type: str
    prices: str
    description: Optional[str] = None
    photos: Optional[str] = None
    videos: Optional[str] = None

class VenueCreate(VenueBase):
    pass

class VenueResponse(VenueBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Booking Schemas

class BookingCreate(BaseModel):
    """Request payload for creating a booking (from the mobile app).

    The **mobile app actually sends snake_case JSON keys** from
    `bookingsApi.createBooking`, e.g. `court_id`, `booking_date`,
    `start_time`, `duration_minutes`.

    To keep things simple and avoid validation confusion, this schema
    now matches those snake_case keys **1:1**. No aliases are used.
    """

    court_id: str
    booking_date: date
    start_time: str  # AM/PM format supported (e.g. "05:00 AM")
    duration_minutes: int
    number_of_players: int = 2
    price_per_hour: float = 200.0
    team_name: Optional[str] = None
    special_requests: Optional[str] = None


class BookingResponse(BaseModel):
    """Response model for bookings, based directly on the DB columns.

    We intentionally use snake_case field names here to match the SQLAlchemy
    model attributes so FastAPI can serialize the `models.Booking` instance
    without response validation errors.
    """

    id: UUID
    user_id: str
    court_id: str
    booking_date: date
    start_time: time
    end_time: time
    duration_minutes: int
    number_of_players: int
    team_name: Optional[str] = None
    special_requests: Optional[str] = None
    price_per_hour: Decimal
    total_amount: Decimal
    status: str
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# OTP / Phone login
class SendOTPRequest(BaseModel):
    phone_number: str

class SendOTPResponse(BaseModel):
    message: str
    success: bool
    verification_id: Optional[str] = None
    otp_code: Optional[str] = None

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp_code: str
    # Optional profile fields to store/update when verifying phone
    full_name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    handedness: Optional[str] = None
    skill_level: Optional[str] = None
    sports: Optional[List[str]] = None
    playing_style: Optional[str] = None

class VerifyOTPResponse(BaseModel):
    access_token: str
    token_type: str

# Admin Data Schemas
class CityResponse(BaseModel):
    id: UUID
    name: str
    short_code: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class GameTypeResponse(BaseModel):
    id: UUID
    name: str
    icon_url: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

# Admin Court Schemas
class AdminCourtBase(BaseModel):
    branch_id: str
    game_type_id: str
    name: str
    price_per_hour: float
    price_conditions: Optional[List[dict]] = []
    unavailability_slots: Optional[List[dict]] = []
    operating_hours: Optional[dict] = {}
    images: Optional[List[str]] = []
    videos: Optional[List[str]] = []
    is_active: Optional[bool] = True

class AdminCourtResponse(AdminCourtBase):
    id: str  # Changed from UUID to str to handle UUID serialization
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

# Coupon Schemas
class CouponValidateRequest(BaseModel):
    coupon_code: str
    total_amount: float

class CouponResponse(BaseModel):
    valid: bool
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
    final_amount: Optional[float] = None
    message: str

class AdminCouponResponse(BaseModel):
    id: str
    coupon_code: str
    discount_percentage: float
    start_date: datetime
    end_date: datetime
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
