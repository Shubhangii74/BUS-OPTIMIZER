#!/usr/bin/env python3
"""
Bus Seat Allocation Optimizer - Startup Script
A simple script to run the Flask application with proper setup.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please run: pip install -r requirements.txt")
        sys.exit(1)

def create_data_directory():
    """Ensure data directory exists"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print("✅ Data directory ready")

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           🚌 Bus Seat Allocation Optimizer 🚌               ║
    ║                                                              ║
    ║              Smart seat allocation for students              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_info():
    """Print application information"""
    info = """
    🎯 Features:
    • Smart seat allocation using Greedy & Knapsack algorithms
    • Zone-based allocation (front/middle/back seats)
    • Real-time dashboard with visual bus layout
    • Modern UI with animations and particles
    
    🌐 Access Points:
    • Landing Page: http://localhost:5000
    • Student Portal: http://localhost:5000/student
    • Admin Dashboard: http://localhost:5000/admin
    
    🔑 Demo Access:
    • Use any credentials for both student and admin login
    • No authentication required for prototype
    
    📊 Data Storage:
    • CSV files in /data directory
    • Auto-generated on first run
    """
    print(info)

def main():
    """Main startup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    if not os.path.exists("venv"):
        print("💡 Tip: Consider using a virtual environment for better isolation")
    
    install_requirements()
    
    # Create data directory
    create_data_directory()
    
    # Print information
    print_info()
    
    # Start the application
    print("🚀 Starting Bus Seat Allocation Optimizer...")
    print("⏳ Please wait while the server starts...")
    
    try:
        # Import and run the Flask app
        from app import app
        print("✅ Server started successfully!")
        print("🌐 Opening browser automatically...")
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Open browser
        webbrowser.open('http://localhost:5000')
        
        print("\n🎉 Application is running!")
        print("📱 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Bus Seat Allocation Optimizer...")
        print("✅ Server stopped successfully!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure no other application is using port 5000")
        sys.exit(1)

if __name__ == "__main__":
    main() 