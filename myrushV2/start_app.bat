@echo off
echo ========================================
echo Starting MyRush Application
echo ========================================
echo.

echo [1/2] Starting Backend Server (Python FastAPI)...
echo Backend will run on http://localhost:5000
echo.
start "MyRush Backend" cmd /k "cd MYRUSH-USER-APP\backend_python && python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload"

echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting Frontend (Expo)...
echo Frontend will open in Expo...
echo.
start "MyRush Frontend" cmd /k "cd MYRUSH-USER-APP\mobile && npm start"

echo.
echo ========================================
echo ✅ Both servers are starting!
echo ========================================
echo.
echo Backend API: http://localhost:5000
echo Backend Docs: http://localhost:5000/docs
echo Frontend: Check Expo window for QR code
echo.
echo Press any key to close this window (servers will keep running)...
pause >nul
