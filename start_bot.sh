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
    echo "This may take a minute..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        echo ""
        echo "Troubleshooting:"
        echo "1. Ensure python3-venv is installed: sudo apt-get install python3-venv"
        echo "2. Check write permissions in this directory"
        echo "3. Ensure you have enough disk space"
        echo ""
        exit 1
    fi
    echo "[OK] Virtual environment created successfully"
    echo ""
else
    echo "[OK] Virtual environment already exists"
fi

# Activate virtual environment
echo "[SETUP] Activating virtual environment..."
set +e  # Don't exit on error for this check
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    echo ""
    echo "The venv folder may be corrupted. Solutions:"
    echo "1. Delete the 'venv' folder: rm -rf venv"
    echo "2. Run this script again"
    echo "3. Check folder permissions"
    echo ""
    exit 1
fi
set -e  # Re-enable exit on error

echo "[OK] Virtual environment activated"
echo "Using: $VIRTUAL_ENV"
echo ""

# Check if dependencies are installed
echo "[SETUP] Checking dependencies..."
set +e  # Don't exit on error for this check
python -c "import streamlit" &> /dev/null
STREAMLIT_INSTALLED=$?
set -e

if [ $STREAMLIT_INSTALLED -ne 0 ]; then
    echo "[SETUP] Installing dependencies - this may take 5-10 minutes..."
    echo "Please be patient, do not close this terminal."
    echo ""
    
    # Upgrade pip first for better stability
    echo "[SETUP] Upgrading pip to latest version..."
    python -m pip install --upgrade pip > /dev/null 2>&1
    
    # Check if TA-Lib is installed
    set +e  # Don't exit on error for this check
    python -c "import talib" &> /dev/null
    TALIB_INSTALLED=$?
    set -e
    
    if [ $TALIB_INSTALLED -ne 0 ]; then
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
        echo "On Ubuntu/Debian:"
        echo "  sudo apt-get install build-essential wget"
        echo "  wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        echo "  tar -xzf ta-lib-0.4.0-src.tar.gz"
        echo "  cd ta-lib/"
        echo "  ./configure --prefix=/usr"
        echo "  make"
        echo "  sudo make install"
        echo "  pip install TA-Lib"
        echo ""
        echo "After installation, run this script again."
        echo ""
        exit 1
    fi
    
    echo "[OK] TA-Lib detected"
    echo ""
    echo "[SETUP] Installing remaining Python packages..."
    echo "Progress: Installing scientific computing packages..."
    
    set +e  # Don't exit on error, we'll handle it
    pip install -r requirements.txt --no-cache-dir
    PIP_EXIT_CODE=$?
    set -e
    
    if [ $PIP_EXIT_CODE -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        echo ""
        echo "Troubleshooting:"
        echo "1. Check your internet connection"
        echo "2. Try running: pip install -r requirements.txt"
        echo "3. Check the error messages above"
        echo "4. On Linux, you may need to install: sudo apt-get install python3-dev build-essential"
        echo ""
        exit 1
    fi
    echo "[OK] All dependencies installed successfully"
else
    echo "[OK] Dependencies already installed"
    echo "[INFO] To update dependencies, delete the venv folder and run this script again"
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

# Create necessary directories if they don't exist
echo "[SETUP] Checking directory structure..."
mkdir -p data logs models reports
echo "[OK] Directory structure ready"

# Check if database needs initialization
if [ ! -f "data/mt5_sentiment.db" ]; then
    echo "[SETUP] Initializing database..."
    set +e  # Don't exit on error for this check
    python -c "from src.database.models import init_database; init_database(); print('[OK] Database initialized')" 2>/dev/null
    DB_INIT_CODE=$?
    set -e
    
    if [ $DB_INIT_CODE -ne 0 ]; then
        echo "[WARNING] Database initialization failed - will retry on first run"
        echo "This is normal if dependencies were just installed"
    else
        echo "[OK] Database initialized successfully"
    fi
else
    echo "[OK] Database already initialized"
fi

echo ""
echo "========================================"
echo "Starting MT5 Sentiment Analysis Bot..."
echo "========================================"
echo ""
echo "[INFO] Starting Python-based Streamlit application"
echo "[INFO] Dashboard will open in your browser automatically"
echo "[INFO] Press Ctrl+C to stop the bot"
echo ""
echo "Launching..."
echo ""

# Start Streamlit with the app and better error handling
set +e  # Don't exit on error, capture exit code
streamlit run app.py --server.headless=true --server.port=8501
STREAMLIT_EXIT_CODE=$?
set -e

# If Streamlit exits, show message
echo ""
echo "========================================"
echo "Bot stopped"
echo "========================================"

if [ $STREAMLIT_EXIT_CODE -ne 0 ]; then
    echo ""
    echo "[WARNING] Application exited with error code: $STREAMLIT_EXIT_CODE"
    echo "Check the logs folder for error details"
    echo ""
fi

echo ""
echo "To restart the bot, run this script again: ./start_bot.sh"
echo ""
