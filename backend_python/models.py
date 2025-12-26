from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, DECIMAL, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime
import uuid as uuid_lib

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, index=True, server_default=func.uuid_generate_v4()) # UUID
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    profile = relationship("Profile", back_populates="user", uselist=False)
    bookings = relationship("Booking", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=False), ForeignKey("users.id"), primary_key=True)
    phone_number = Column(String(20), unique=True, index=True)
    full_name = Column(String(100))
    age = Column(Integer)
    city = Column(String(100))
    gender = Column(String(20))
    handedness = Column(String(20))
    skill_level = Column(String(50))
    sports = Column(JSON) # Store as JSON array
    playing_style = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="profile")

class OtpVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), index=True)
    otp_code = Column(String(6))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    is_verified = Column(Boolean, default=False)

class Venue(Base):
    __tablename__ = "adminvenues"

    id = Column(String(36), primary_key=True, index=True)
    court_name = Column(String(255), index=True)
    location = Column(String(255), index=True)
    city = Column(String(100), index=True)
    game_type = Column(String(255))  # Comma separated if multiple
    prices = Column(String(255))
    description = Column(Text, nullable=True)
    photos = Column(Text, nullable=True)  # JSON string or comma separated
    videos = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # bookings = relationship("Booking", back_populates="venue")

class Booking(Base):
    __tablename__ = "booking"

    id = Column(UUID(as_uuid=False), primary_key=True, index=True, server_default=func.uuid_generate_v4()) # UUID
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    court_id = Column(UUID(as_uuid=False), nullable=False)  # No FK - references admin_courts
    booking_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    number_of_players = Column(Integer, default=2)
    team_name = Column(String(100), nullable=True)
    special_requests = Column(Text, nullable=True)
    price_per_hour = Column(DECIMAL(10, 2), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    # Business rule: a booking is considered CONFIRMED as soon as it is
    # successfully created via the app. Payment can still be pending.
    status = Column(String(20), default='confirmed')
    payment_id = Column(String(100))
    payment_status = Column(String(20), default='pending')
    admin_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="bookings")
    # venue = relationship("Venue", back_populates="bookings")

class AdminCity(Base):
    __tablename__ = "admin_cities"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), index=True)
    short_code = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AdminGameType(Base):
    __tablename__ = "admin_game_types"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100), index=True)
    short_code = Column(String(10))
    description = Column(Text)
    icon = Column(String(100))
    icon_url = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AdminCourt(Base):
    __tablename__ = "admin_courts"

    id = Column(String(36), primary_key=True, index=True)
    branch_id = Column(String(36), nullable=False)  # Foreign key to admin_branches
    game_type_id = Column(String(36), nullable=False)  # Foreign key to admin_game_types
    name = Column(String(255), nullable=False)  # Court name
    price_per_hour = Column(DECIMAL(10, 2), nullable=False)  # Price per hour
    price_conditions = Column(JSON, nullable=True, default=list)  # JSONB array
    unavailability_slots = Column(JSON, nullable=True, default=list)  # JSONB array
    operating_hours = Column(JSON, nullable=True, default=dict)  # JSONB object for operating hours
    images = Column(JSON, nullable=True, default=list)  # TEXT array
    videos = Column(JSON, nullable=True, default=list)  # TEXT array
    is_active = Column(Boolean, nullable=True, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
