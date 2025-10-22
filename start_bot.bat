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
    echo This may take a minute...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo.
        echo Troubleshooting:
        echo 1. Ensure you have write permissions in this directory
        echo 2. Try running as Administrator
        echo 3. Check if antivirus is blocking the operation
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully
    echo.
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    echo.
    echo The venv folder may be corrupted. Solutions:
    echo 1. Delete the 'venv' folder and run this script again
    echo 2. Check folder permissions
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo Using: !VIRTUAL_ENV!
echo.

REM Check if dependencies are installed
echo [SETUP] Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Installing dependencies - this may take 5-10 minutes...
    echo Please be patient, do not close this window.
    echo.
    
    REM Upgrade pip first for better stability
    echo [SETUP] Upgrading pip to latest version...
    python -m pip install --upgrade pip >nul 2>&1
    
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
            echo OPTION 1 - Download wheel file (RECOMMENDED):
            echo   1. Go to: https://github.com/cgohlke/talib-build/releases
            echo   2. Download the .whl file matching your Python version
            echo      Example for Python 3.10: TA_Lib-0.4.XX-cp310-cp310-win_amd64.whl
            echo      Example for Python 3.11: TA_Lib-0.4.XX-cp311-cp311-win_amd64.whl
            echo   3. Run: pip install path\to\downloaded-file.whl
            echo.
            echo OPTION 2 - Try manual install:
            echo   pip install Ta-lib
            echo.
            echo After installation, run this script again.
            echo.
            pause
            exit /b 1
        )
    )
    echo [OK] TA-Lib installed successfully
    
    echo [SETUP] Installing remaining Python packages...
    echo Progress: Installing scientific computing packages...
    pip install -r requirements.txt --no-cache-dir
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo.
        echo Troubleshooting:
        echo 1. Check your internet connection
        echo 2. Try running: pip install -r requirements.txt
        echo 3. Check the error messages above
        echo.
        pause
        exit /b 1
    )
    echo [OK] All dependencies installed successfully
) else (
    echo [OK] Dependencies already installed
    echo [INFO] To update dependencies, delete the venv folder and run this script again
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

REM Create necessary directories if they don't exist
echo [SETUP] Checking directory structure...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "models" mkdir models
if not exist "reports" mkdir reports
echo [OK] Directory structure ready

REM Check if database needs initialization
if not exist "data\mt5_sentiment.db" (
    echo [SETUP] Initializing database...
    python -c "from src.database.models import init_database; init_database(); print('[OK] Database initialized')" 2>nul
    if errorlevel 1 (
        echo [WARNING] Database initialization failed - will retry on first run
        echo This is normal if dependencies were just installed
    ) else (
        echo [OK] Database initialized successfully
    )
) else (
    echo [OK] Database already initialized
)

echo.
echo ========================================
echo Starting MT5 Sentiment Analysis Bot...
echo ========================================
echo.
echo [INFO] Starting Python-based Streamlit application
echo [INFO] Dashboard will open in your browser automatically
echo [INFO] Press Ctrl+C to stop the bot
echo.
echo Launching...
echo.

REM Start Streamlit with the app and better error handling
streamlit run app.py --server.headless=true --server.port=8501
set STREAMLIT_EXIT_CODE=%errorlevel%

REM If Streamlit exits, show message
echo.
echo ========================================
echo Bot stopped
echo ========================================

if %STREAMLIT_EXIT_CODE% NEQ 0 (
    echo.
    echo [WARNING] Application exited with error code: %STREAMLIT_EXIT_CODE%
    echo Check the logs folder for error details
    echo.
)

echo.
echo To restart the bot, run this script again.
echo.
pause

endlocal
