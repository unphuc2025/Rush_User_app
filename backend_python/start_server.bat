@echo off
echo Starting MyRush Python Backend...
echo.

REM Use the Python installation
"C:\Users\Z BOOK\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn main:app --reload --host 0.0.0.0 --port 5000
