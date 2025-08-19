#!/bin/bash

# Ultimate Utility Tools - Run Script

echo "🛠️  Starting Ultimate Utility Tools..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p static/uploads logs

# Run the application
echo "🚀 Starting the server..."
echo "📱 Open http://localhost:8000 in your browser"
echo "📚 API docs available at http://localhost:8000/api/docs"
echo "🛑 Press Ctrl+C to stop the server"

python main.py