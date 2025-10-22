#!/bin/bash
# ========================================
# MT5 Sentiment Analysis Bot Launcher
# Anaconda/Miniconda version for Linux/Mac
# ========================================

echo ""
echo "========================================"
echo "MT5 Sentiment Analysis Bot (Conda)"
echo "========================================"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "[ERROR] Conda is not installed or not in PATH"
    echo "Please install Anaconda or Miniconda from:"
    echo "  Anaconda: https://www.anaconda.com/products/distribution"
    echo "  Miniconda: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "[OK] Conda found"
echo ""

# Check if environment exists
ENV_NAME="mt5-sentiment-bot"
conda env list | grep -q "^${ENV_NAME} " &> /dev/null
ENV_EXISTS=$?

if [ $ENV_EXISTS -ne 0 ]; then
    echo "[SETUP] Creating conda environment from environment.yml..."
    echo "This may take several minutes..."
    echo ""
    conda env create -f environment.yml
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create conda environment"
        exit 1
    fi
    echo ""
    echo "[OK] Conda environment created"
else
    echo "[OK] Conda environment '${ENV_NAME}' already exists"
    echo ""
    
    # Ask if user wants to update
    read -p "Update environment from environment.yml? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "[SETUP] Updating conda environment..."
        conda env update -f environment.yml --prune
        if [ $? -ne 0 ]; then
            echo "[WARNING] Failed to update environment (continuing anyway)"
        else
            echo "[OK] Environment updated"
        fi
    fi
fi

echo ""

# Activate conda environment
echo "[SETUP] Activating conda environment..."

# Get the conda base path
CONDA_BASE=$(conda info --base)

# Source conda.sh to enable conda activate
source "${CONDA_BASE}/etc/profile.d/conda.sh"

conda activate ${ENV_NAME}
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate conda environment"
    echo "Try running: conda activate ${ENV_NAME}"
    exit 1
fi

echo "[OK] Conda environment activated"
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

# Create necessary directories
mkdir -p data logs models reports

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
