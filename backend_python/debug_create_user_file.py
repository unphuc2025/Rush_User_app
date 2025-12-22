from database import SessionLocal
import models
import crud
import schemas
import uuid
import sys

def debug_create_user():
    with open("debug_create_output.txt", "w") as f:
        db = SessionLocal()
        phone_number = "+916300766577"
        
        f.write(f"Testing user creation for: {phone_number}\n")
        
        try:
            # 1. Check if user exists
            user = crud.get_user_by_phone(db, phone_number)
            if user:
                f.write(f"User already exists: {user.id}\n")
            else:
                f.write("User not found, attempting to create...\n")
                
                # Simulate verify_otp logic
                profile_payload = {
                    "full_name": "Test User",
                    "city": "Test City",
                    "phone_number": phone_number
                }
                
                # Create user
                user = crud.create_user_with_phone(db, phone_number, profile_payload)
                f.write(f"User created successfully: {user.id}\n")
                
                # Create profile
                profile_create = schemas.ProfileCreate(**profile_payload)
                profile = crud.create_or_update_profile(db, profile_create, user.id)
                f.write(f"Profile created successfully: {profile.id}\n")
                
            # 2. Verify we can read it back
            f.write("Verifying read...\n")
            user_read = db.query(models.User).filter(models.User.id == user.id).first()
            f.write(f"   User: {user_read.first_name} {user_read.last_name}\n")
            f.write(f"   Profile: {user_read.profile.city if user_read.profile else 'None'}\n")
            
        except Exception as e:
            f.write(f"ERROR: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        finally:
            db.close()

if __name__ == "__main__":
    debug_create_user()
