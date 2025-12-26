from database import SessionLocal
import models
import crud
import schemas
import uuid
import sys

def debug_api_flow():
    with open("debug_api_flow.txt", "w", encoding="utf-8") as f:
        db = SessionLocal()
        phone_number = "+916300766577"
        email = f"{phone_number}@phone.myrush.app"
        
        f.write(f"Testing API flow for: {email}\n")
        
        try:
            # 1. Simulate get_current_user (by email)
            f.write("1. Calling get_user_by_email...\n")
            user = crud.get_user_by_email(db, email)
            
            if not user:
                f.write("User not found! (This is unexpected if verify_otp succeeded)\n")
                return
                
            f.write(f"User found: {user.id}\n")
            f.write(f"   Phone: {user.phone_number}\n")
            
            # 2. Simulate get_profile endpoint
            f.write("2. Calling crud.get_profile...\n")
            profile = crud.get_profile(db, user.id)
            
            if not profile:
                f.write("Profile not found!\n")
            else:
                f.write(f"Profile found: {profile.id}\n")
                f.write(f"   Phone: {profile.phone_number}\n")
                
                # 3. Simulate Pydantic validation
                f.write("3. Validating against ProfileResponse...\n")
                try:
                    resp = schemas.ProfileResponse.from_orm(profile)
                    f.write(f"Validation successful: {resp.json()}\n")
                except Exception as e:
                    f.write(f"Validation failed: {e}\n")

        except Exception as e:
            f.write(f"ERROR: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        finally:
            db.close()

if __name__ == "__main__":
    debug_api_flow()
