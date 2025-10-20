#!/bin/bash
# ========================================
# MT5 Sentiment Analysis Bot Launcher
# For Linux/Mac users
# ========================================
# This script handles all setup and starts the bot automatically

echo ""
echo "========================================"
echo "MT5 Sentiment Analysis Bot"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python found"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[SETUP] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created"
fi

# Activate virtual environment
echo "[SETUP] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

echo "[OK] Virtual environment activated"
echo ""

# Check if dependencies are installed
echo "[SETUP] Checking dependencies..."
python -c "import streamlit" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[SETUP] Installing dependencies (this may take a few minutes)..."
    echo ""
    
    # Check if TA-Lib is installed
    python -c "import talib" &> /dev/null
    if [ $? -ne 0 ]; then
        echo ""
        echo "========================================"
        echo "WARNING: TA-Lib not detected"
        echo "========================================"
        echo "TA-Lib must be installed manually before proceeding."
        echo ""
        echo "On macOS:"
        echo "  brew install ta-lib"
        echo "  pip install TA-Lib"
        echo ""
        echo "On Linux:"
        echo "  See SETUP_GUIDE.md for instructions"
        echo ""
        exit 1
    fi
    
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "[OK] Dependencies installed"
else
    echo "[OK] Dependencies already installed"
fi

echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found"
    echo ""
    if [ -f ".env.example" ]; then
        echo "[SETUP] Creating .env from .env.example..."
        cp .env.example .env
        echo "[OK] .env file created"
        echo ""
        echo "========================================"
        echo "ACTION REQUIRED"
        echo "========================================"
        echo "Please edit .env file with your MT5 credentials:"
        echo "  - MT5_LOGIN"
        echo "  - MT5_PASSWORD"
        echo "  - MT5_SERVER"
        echo ""
        echo "After editing, run this script again."
        echo ""
        
        # Try to open in default editor
        if command -v nano &> /dev/null; then
            read -p "Press Enter to edit .env file (or Ctrl+C to exit)..."
            nano .env
        fi
        exit 0
    else
        echo "[ERROR] .env.example not found"
        exit 1
    fi
fi

echo "[OK] Configuration file found"
echo ""

# Check if database needs initialization
if [ ! -f "data/mt5_sentiment.db" ]; then
    echo "[SETUP] Initializing database..."
    python -c "from src.database.models import init_database; init_database(); print('[OK] Database initialized')"
    if [ $? -ne 0 ]; then
        echo "[WARNING] Database initialization failed (will retry on first run)"
    fi
fi

echo ""
echo "========================================"
echo "Starting MT5 Sentiment Analysis Bot..."
echo "========================================"
echo ""
echo "Dashboard will open in your browser automatically"
echo "Press Ctrl+C to stop the bot"
echo ""

# Start Streamlit with the app
streamlit run app.py

# If Streamlit exits, show message
echo ""
echo "========================================"
echo "Bot stopped"
echo "========================================"
