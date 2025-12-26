from database import SessionLocal
import models
import crud
import schemas
import uuid

def debug_create_user():
    db = SessionLocal()
    phone_number = "+916300766577"
    
    print(f"🔍 Testing user creation for: {phone_number}")
    
    try:
        # 1. Check if user exists
        user = crud.get_user_by_phone(db, phone_number)
        if user:
            print(f"✅ User already exists: {user.id}")
        else:
            print("⚠️ User not found, attempting to create...")
            
            # Simulate verify_otp logic
            profile_payload = {
                "full_name": "Test User",
                "city": "Test City",
                "phone_number": phone_number
            }
            
            # Create user
            # Note: create_user_with_phone calls create_user which sets password_hash
            user = crud.create_user_with_phone(db, phone_number, profile_payload)
            print(f"✅ User created successfully: {user.id}")
            
            # Create profile
            profile_create = schemas.ProfileCreate(**profile_payload)
            profile = crud.create_or_update_profile(db, profile_create, user.id)
            print(f"✅ Profile created successfully: {profile.id}")
            
        # 2. Verify we can read it back
        print("🔍 Verifying read...")
        user_read = db.query(models.User).filter(models.User.id == user.id).first()
        print(f"   User: {user_read.first_name} {user_read.last_name}")
        print(f"   Profile: {user_read.profile.city if user_read.profile else 'None'}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_create_user()
