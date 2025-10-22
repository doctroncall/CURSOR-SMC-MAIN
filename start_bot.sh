#!/bin/bash
# ========================================
# MT5 Sentiment Analysis Bot Launcher
# Enhanced Python Stable Version
# For Linux/Mac users
# ========================================
# This script handles all setup and starts the bot automatically

set -e  # Exit on error (we'll handle errors manually where needed)

echo ""
echo "========================================"
echo "MT5 Sentiment Analysis Bot (Python)"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo ""
    echo "Please install Python 3.10+ from https://www.python.org/downloads/"
    echo ""
    echo "On Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    echo "On macOS: brew install python3"
    echo ""
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "[OK] Python found - Version $PYTHON_VERSION"

# Extract major and minor version
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

# Check if Python version is 3.10 or higher
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "[ERROR] Python 3.10+ required. Current version: $PYTHON_VERSION"
    echo "Please upgrade Python from https://www.python.org/downloads/"
    exit 1
fi

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
