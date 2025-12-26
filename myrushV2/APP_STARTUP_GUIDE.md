# MyRush App - Startup Guide

## ✅ Application Successfully Configured!

Your MyRush application is now ready to run with:
- **Backend**: Python FastAPI with PostgreSQL (Supabase)
- **Frontend**: React Native with Expo

---

## 🚀 Quick Start

### Option 1: Use the Automated Script (Recommended)
Simply double-click or run:
```bash
.\start_app.bat
```

This will automatically:
1. Start the backend server on `http://localhost:5000`
2. Start the Expo development server
3. Open two separate terminal windows for each service

---

## 📋 Manual Startup (Alternative)

### Step 1: Start Backend Server
Open a terminal and run:
```bash
cd MYRUSH-USER-APP/backend_python
python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

### Step 2: Start Frontend (Expo)
Open another terminal and run:
```bash
cd MYRUSH-USER-APP/mobile
npm start
```

---

## 🔗 Access Points

### Backend API
- **API Base URL**: http://localhost:5000
- **API Documentation**: http://localhost:5000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:5000/redoc

### Frontend (Expo)
- After running `npm start`, you'll see:
  - QR code to scan with Expo Go app (for physical devices)
  - Options to run on Android/iOS emulator
  - Web option (press `w`)

---

## 📱 Testing on Mobile Device

1. Install **Expo Go** app on your phone:
   - [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)
   - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

2. Make sure your phone and computer are on the **same WiFi network**

3. Scan the QR code shown in the Expo terminal

---

## 🗄️ Database Configuration

### PostgreSQL (Supabase) - Already Connected ✅
- **Database**: MYRUSH
- **Host**: db.vqglejkydwtopmllymuf.supabase.co
- **Connection**: SSL enabled
- **Status**: ✅ Successfully tested and connected

### Available Tables:
- `users` - User authentication
- `profiles` - User profiles
- `otp_verifications` - OTP login
- `booking` - Booking records
- `admin_venues` - Venue management
- `admin_branches` - Branch locations
- `admin_courts` - Court details
- And more...

---

## 🔧 Configuration Files

### Backend (.env)
Location: `MYRUSH-USER-APP/backend_python/.env`
```
DATABASE_URL=postgresql://postgres:***@db.vqglejkydwtopmllymuf.supabase.co:5432/MYRUSH?sslmode=require
```

### Frontend (.env)
Location: `MYRUSH-USER-APP/mobile/.env`
```
API_BASE_URL=http://localhost:5000
API_VERSION=v1
APP_NAME=MyRush
APP_ENV=development
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem**: Backend won't start
```bash
# Check if Python is installed
python --version

# Reinstall dependencies
cd MYRUSH-USER-APP/backend_python
pip install -r requirements.txt
```

**Problem**: Database connection error
```bash
# Test PostgreSQL connection
cd MYRUSH-USER-APP/backend_python
python test_postgres_connection.py
```

### Frontend Issues

**Problem**: Expo won't start
```bash
# Reinstall dependencies
cd MYRUSH-USER-APP/mobile
npm install

# Clear cache and restart
npm start --clear
```

**Problem**: Can't connect to backend
- Make sure backend is running on port 5000
- Check that `API_BASE_URL` in mobile/.env is correct
- For physical devices, use your computer's IP instead of localhost

---

## 📊 Monitoring

### Backend Logs
- Check the "MyRush Backend" terminal window
- API requests will be logged in real-time
- Database queries are logged with details

### Frontend Logs
- Check the "MyRush Frontend" terminal window
- Expo DevTools will show in browser
- Use React Native Debugger for advanced debugging

---

## 🎯 Next Steps

1. **Test the API**: Visit http://localhost:5000/docs
2. **Run the mobile app**: Scan QR code with Expo Go
3. **Test authentication**: Try OTP login feature
4. **Browse venues**: Check venue listing and booking flow
5. **Check profile**: View and edit user profile

---

## 📞 Support

If you encounter any issues:
1. Check the terminal logs for error messages
2. Verify all dependencies are installed
3. Ensure PostgreSQL connection is working
4. Make sure ports 5000 (backend) and 8081 (Expo) are not in use

---

## ✨ Features Available

- ✅ OTP-based authentication
- ✅ User profile management
- ✅ Venue browsing and search
- ✅ Court booking system
- ✅ Booking history
- ✅ Real-time availability
- ✅ PostgreSQL database integration

---

**Last Updated**: December 10, 2025
**Status**: Ready for Development ✅
