@echo off
echo Starting MyRush Backend Server...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment (from parent directory)
call ..\..\.venv\Scripts\activate.bat

REM Start the server
echo Server starting at http://localhost:8000
echo API Documentation at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
