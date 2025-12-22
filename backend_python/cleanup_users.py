"""
Clean up script to remove any users with bad password hashes
Run this to clear the database before testing
"""
from database import SessionLocal
import models

def cleanup_phone_users():
    db = SessionLocal()
    try:
        # Delete all phone-based users (they'll be recreated on next OTP login)
        # Match both old .local and new .app domains
        phone_users = db.query(models.User).filter(
            (models.User.email.like('%@phone.local')) | 
            (models.User.email.like('%@phone.myrush.app'))
        ).all()
        
        print(f"Found {len(phone_users)} phone users to clean up")
        
        for user in phone_users:
            print(f"Deleting user: {user.email}")
            # Delete associated profile first (if cascade doesn't work)
            profile = db.query(models.Profile).filter(models.Profile.id == user.id).first()
            if profile:
                db.delete(profile)
            db.delete(user)
        
        db.commit()
        print("✅ Cleanup complete!")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_phone_users()
