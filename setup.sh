#!/bin/bash

# Setup script for NDA Agno PandaDoc Integration

echo "🐼 Setting up PandaDoc API Integration with Agno Framework"
echo "========================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your PandaDoc API key."
    echo "📝 Edit .env file: nano .env"
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🚀 Setup complete! Next steps:"
echo "1. Edit .env file and add your PandaDoc API key"
echo "2. Run: python main.py"
echo ""
echo "🔑 Get your API key from: https://developers.pandadoc.com/"
