#!/usr/bin/env python3
"""
Startup script for Ultimate Utility Tools
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    directories = [
        "static/uploads",
        "logs",
        "backend/utils"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Ultimate Utility Tools server...")
    print("📱 Open http://localhost:8000 in your browser")
    print("📚 API docs available at http://localhost:8000/api/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except ImportError:
        print("❌ uvicorn not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

def main():
    """Main startup function"""
    print("🛠️  Ultimate Utility Tools - Startup")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    create_directories()
    start_server()

if __name__ == "__main__":
    main()