# MyRush Backend Migration Guide: Node.js → Python/FastAPI

## Current Status

✅ Python backend code created with FastAPI  
✅ MySQL database schema designed  
❌ Python not installed on system  
❌ MySQL CLI not in PATH  

## What You Need to Install

### 1. Install Python (Required)

**Option A: Download from Python.org (Recommended)**
1. Go to https://www.python.org/downloads/
2. Download Python 3.11 or 3.12
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Restart your terminal/command prompt

**Option B: Using Microsoft Store**
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click Install

### 2. Verify Python Installation

After installation, run:
```powershell
python --version
pip --version
```

### 3. Install Backend Dependencies

Once Python is installed:
```powershell
cd "c:\Users\Z BOOK\Downloads\MyRush-New\MYRUSH-USER-APP\backend_python"

# Install dependencies
pip install -r requirements.txt
```

### 4. Setup MySQL Database

**Option A: Using MySQL Workbench (GUI)**
1. Open MySQL Workbench
2. Connect to your MySQL server (localhost:3308)
   - Username: root
   - Password: 9640351007Ajay@
3. Open the SQL file: `migrations/001_create_tables.sql`
4. Execute it to create all tables

**Option B: Using Command Line (if MySQL CLI is available)**
```powershell
mysql -u root -p -P 3308 -h 127.0.0.1 < migrations/001_create_tables.sql
# Enter password when prompted: 9640351007Ajay@
```

**Option C: Add MySQL to PATH**
If you have MySQL installed but it's not in PATH:
1. Find your MySQL installation folder (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin`)
2. Add it to your system PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add MySQL bin directory

### 5. Run the Python Backend

```powershell
# Make sure you're in the backend_python directory
cd "c:\Users\Z BOOK\Downloads\MyRush-New\MYRUSH-USER-APP\backend_python"

# Start the server
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns JWT token)
- `GET /auth/profile` - Get current user profile

### Profile
- `POST /profile/` - Create or update user profile
- `GET /profile/` - Get user profile

### Bookings
- `POST /bookings/` - Create new booking
- `GET /bookings/` - Get all user bookings

## Database Tables Created

1. **users** - User authentication (id, email, password_hash, first_name, last_name)
2. **profiles** - User profiles (phone_number, full_name, age, city, gender, etc.)
3. **otp_verifications** - Phone OTP verification
4. **bookings** - Booking details (venue_id, booking_date, times, status, payment)

## Next Steps After Backend is Running

1. Update mobile app API endpoint:
   - Replace Supabase URL with `http://localhost:8000` (or your machine IP for physical devices)
   - Update API calls to use new endpoint structure

2. Test the API:
   - Visit `http://localhost:8000/docs` for interactive API testing
   - All endpoints are documented with Swagger UI

## Troubleshooting

**"python is not recognized"**
- Python is not installed or not in PATH
- Follow installation steps above

**"mysql is not recognized"**
- MySQL CLI not in PATH
- Use MySQL Workbench GUI instead
- Or add MySQL bin directory to PATH

**Database connection error**
- Verify MySQL server is running on port 3308
- Check credentials in `.env` file
- Ensure database `myrush` exists

**Port 8000 already in use**
- Change port: `uvicorn main:app --reload --port 8001`

## Migration Checklist

- [ ] Install Python 3.11+
- [ ] Install backend dependencies (`pip install -r requirements.txt`)
- [ ] Create database schema (run `001_create_tables.sql`)
- [ ] Start Python backend (`uvicorn main:app --reload`)
- [ ] Test API at http://localhost:8000/docs
- [ ] Update mobile app API endpoints
- [ ] Test mobile app with new backend

## Configuration Files

- `.env` - Environment variables (database URL, secret key)
- `requirements.txt` - Python dependencies
- `models.py` - Database models
- `main.py` - FastAPI application entry point
- `migrations/001_create_tables.sql` - Database schema
