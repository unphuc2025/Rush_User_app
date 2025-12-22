# MyRush Backend - Python/FastAPI + MySQL

## ✅ Migration Complete!

### What Was Done:
- ✅ Deleted old Node.js backend
- ✅ Python/FastAPI backend is now active
- ✅ Connected to MySQL database at `127.0.0.1:3308`
- ✅ Using existing database tables: users, profiles, otp_verifications, bookings

### Backend Location:
```
MYRUSH-USER-APP/backend_python/
```

### Running the Backend:

**Option 1: Using batch scripts**
```powershell
cd "c:\Users\Z BOOK\Downloads\MyRush-New\MYRUSH-USER-APP\backend_python"
.\run.bat
```

**Option 2: Manual activation**
```powershell
cd "c:\Users\Z BOOK\Downloads\MyRush-New\MYRUSH-USER-APP\backend_python"
.\venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints:

**Base URL:** `http://localhost:8000`

**Authentication:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (get JWT token)
- `GET /auth/profile` - Get user profile (requires auth)

**Profile:**
- `POST /profile/` - Create/update profile (requires auth)
- `GET /profile/` - Get profile (requires auth)

**Bookings:**
- `POST /bookings/` - Create booking (requires auth)
- `GET /bookings/` - List user bookings (requires auth)

**Documentation:**
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Testing Database Connection:

```powershell
cd backend_python
python test_db_connection.py
```

This will verify:
- ✅ Connection to MySQL
- ✅ Database `myrush` is accessible
- ✅ All 4 tables exist (users, profiles, otp_verifications, bookings)
- ✅ Show row counts for each table

### Database Configuration:

Location: `backend_python/.env`
```
DATABASE_URL=mysql+mysqlconnector://root:9640351007Ajay%40@127.0.0.1:3308/myrush
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Next Steps:

1. **Start the backend:**
   ```powershell
   cd backend_python
   .\run.bat
   ```

2. **Test the API:**
   - Visit `http://localhost:8000/docs`
   - Try the endpoints using Swagger UI

3. **Update Mobile App:**
   - Change API base URL from Supabase to `http://localhost:8000`
   - Update API calls to use new endpoint structure
   - For Android emulator: use `http://10.0.2.2:8000`
   - For physical device: use your PC's IP address (e.g., `http://192.168.1.x:8000`)

### Project Structure:

```
backend_python/
├── main.py                 # FastAPI app entry point
├── database.py             # Database connection
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── crud.py                 # Database operations
├── routers/
│   ├── auth.py            # Authentication endpoints
│   ├── profile.py         # Profile endpoints
│   └── bookings.py        # Booking endpoints
├── migrations/
│   └── 001_create_tables.sql  # Database schema
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── setup.bat              # Setup script
├── run.bat                # Run server script
└── test_db_connection.py  # Database test script
```

### Troubleshooting:

**Backend won't start:**
- Make sure virtual environment is activated
- Check if port 8000 is available
- Verify MySQL server is running

**Database connection error:**
- Check MySQL is running on port 3308
- Verify credentials in `.env` file
- Ensure database `myrush` exists

**Mobile app can't connect:**
- Check firewall settings
- Use correct IP address (not localhost for physical devices)
- Ensure backend is running

### Tech Stack:

- **Backend Framework:** FastAPI (Python)
- **Database:** MySQL 8.0
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **API Documentation:** Swagger UI / ReDoc (auto-generated)
