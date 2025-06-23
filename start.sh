#!/bin/bash

# Bus Seat Allocation Optimizer - Startup Script for Unix/Linux/Mac

echo ""
echo "========================================"
echo "   Bus Seat Allocation Optimizer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python found! Installing requirements..."
pip3 install -r requirements.txt

echo ""
echo "Starting the application..."
echo ""
echo "The application will open in your browser automatically."
echo "If it doesn't open, go to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 run.py 