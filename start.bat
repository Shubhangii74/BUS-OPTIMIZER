@echo off
title Bus Seat Allocation Optimizer
color 0A

echo.
echo ========================================
echo    Bus Seat Allocation Optimizer
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found! Installing requirements...
pip install -r requirements.txt

echo.
echo Starting the application...
echo.
echo The application will open in your browser automatically.
echo If it doesn't open, go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause 