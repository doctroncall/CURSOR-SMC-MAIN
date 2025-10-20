@echo off
REM ========================================
REM MT5 Sentiment Analysis Bot Launcher
REM ========================================
REM This script handles all setup and starts the bot automatically

echo.
echo ========================================
echo MT5 Sentiment Analysis Bot
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM Check if dependencies are installed
echo [SETUP] Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Installing dependencies (this may take a few minutes)...
    echo.
    
    REM Check if TA-Lib is installed
    python -c "import talib" >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ========================================
        echo WARNING: TA-Lib not detected
        echo ========================================
        echo TA-Lib must be installed manually before proceeding.
        echo.
        echo Please follow these steps:
        echo 1. Download TA-Lib wheel from:
        echo    https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
        echo 2. Install with: pip install [downloaded-wheel-file]
        echo 3. Run this script again
        echo.
        pause
        exit /b 1
    )
    
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies already installed
)

echo.

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found
    echo.
    if exist ".env.example" (
        echo [SETUP] Creating .env from .env.example...
        copy .env.example .env >nul
        echo [OK] .env file created
        echo.
        echo ========================================
        echo ACTION REQUIRED
        echo ========================================
        echo Please edit .env file with your MT5 credentials:
        echo   - MT5_LOGIN
        echo   - MT5_PASSWORD
        echo   - MT5_SERVER
        echo.
        echo After editing, run this script again.
        pause
        notepad .env
        exit /b 0
    ) else (
        echo [ERROR] .env.example not found
        pause
        exit /b 1
    )
)

echo [OK] Configuration file found
echo.

REM Check if database needs initialization
if not exist "data\mt5_sentiment.db" (
    echo [SETUP] Initializing database...
    python -c "from src.database.models import init_database; init_database(); print('[OK] Database initialized')"
    if errorlevel 1 (
        echo [WARNING] Database initialization failed (will retry on first run)
    )
)

echo.
echo ========================================
echo Starting MT5 Sentiment Analysis Bot...
echo ========================================
echo.
echo Dashboard will open in your browser automatically
echo Press Ctrl+C to stop the bot
echo.

REM Start Streamlit with the app
streamlit run app.py

REM If Streamlit exits, show message
echo.
echo ========================================
echo Bot stopped
echo ========================================
pause
