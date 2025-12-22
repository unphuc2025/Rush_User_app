from database import SessionLocal
import models
from sqlalchemy.orm import joinedload
import sys

def debug_profile_fetch():
    db = SessionLocal()
    phone_number = "+916300766577"
    
    print(f"🔍 Searching for user with phone: {phone_number}")
    
    try:
        # 1. Find profile first (since phone is in profile)
        profile = db.query(models.Profile).filter(models.Profile.phone_number == phone_number).first()
        
        if not profile:
            print("❌ Profile not found!")
            # Try finding user by email pattern
            email = f"{phone_number}@phone.myrush.app"
            print(f"🔍 Searching for user by email: {email}")
            user = db.query(models.User).filter(models.User.email == email).first()
            if user:
                print(f"✅ User found: {user.id}")
                print(f"   Email: {user.email}")
                print(f"   Profile relation: {user.profile}")
            else:
                print("❌ User not found either!")
            return

        print(f"✅ Profile found: {profile.id}")
        print(f"   Phone: {profile.phone_number}")
        
        # 2. Get User via profile
        user = profile.user
        if user:
            print(f"✅ User found via profile: {user.id}")
            print(f"   Email: {user.email}")
            
            # 3. Test serialization (accessing fields)
            print("🔍 Testing serialization...")
            data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "profile": {
                    "phone": user.profile.phone_number,
                    "city": user.profile.city
                }
            }
            print(f"✅ Serialization successful: {data}")
        else:
            print("❌ User relationship on profile is None!")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_profile_fetch()
