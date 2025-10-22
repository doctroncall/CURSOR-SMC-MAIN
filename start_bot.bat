@echo off
REM ========================================
REM MT5 Sentiment Analysis Bot Launcher
REM Enhanced Python Stable Version
REM ========================================
REM This script handles all setup and starts the bot automatically

setlocal enabledelayedexpansion

echo.
echo ========================================
echo MT5 Sentiment Analysis Bot (Python)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version and validate
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python found - Version %PYTHON_VERSION%

REM Extract major and minor version
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

REM Check if Python version is 3.10 or higher
if %PYTHON_MAJOR% LSS 3 (
    echo [ERROR] Python 3.10+ required. Current version: %PYTHON_VERSION%
    echo Please upgrade Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
if %PYTHON_MAJOR% EQU 3 if %PYTHON_MINOR% LSS 10 (
    echo [WARNING] Python 3.10+ recommended. Current version: %PYTHON_VERSION%
    echo The bot may work but some features might be unstable.
    echo.
    choice /C YN /M "Continue anyway"
    if errorlevel 2 exit /b 1
)

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
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Installing dependencies this may take a few minutes...
    echo.
    
    REM Try to install TA-Lib first
    echo [SETUP] Attempting to install TA-Lib...
    pip install Ta-lib >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] TA-Lib pip install failed, trying alternative...
        pip install TA-Lib >nul 2>&1
    )
    
    REM Check if TA-Lib is now installed
    pip show Ta-lib >nul 2>&1
    if errorlevel 1 (
        pip show TA-Lib >nul 2>&1
        if errorlevel 1 (
            echo.
            echo ========================================
            echo WARNING: TA-Lib installation failed
            echo ========================================
            echo TA-Lib is required but could not be installed automatically.
            echo.
            echo Please try ONE of these options:
            echo.
            echo OPTION 1 - Try manual install:
            echo   pip install Ta-lib
            echo.
            echo OPTION 2 - Download wheel file:
            echo   1. Go to: https://github.com/cgohlke/talib-build/releases
            echo   2. Download the .whl file for Python 3.13
            echo   3. Run: pip install path\to\downloaded-file.whl
            echo.
            echo After installation, run this script again.
            echo.
            pause
            exit /b 1
        )
    )
    echo [OK] TA-Lib installed
    
    echo [SETUP] Installing remaining Python packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] All dependencies installed
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

REM Create data directory if it doesn't exist
if not exist "data" mkdir data

REM Check if database needs initialization
if not exist "data\mt5_sentiment.db" (
    echo [SETUP] Initializing database...
    python -c "from src.database.models import init_database; init_database(); print('[OK] Database initialized')" 2>nul
    if errorlevel 1 (
        echo [WARNING] Database initialization failed will retry on first run
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
