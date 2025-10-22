@echo off
REM ========================================
REM MT5 Sentiment Analysis Bot Launcher
REM Anaconda/Miniconda version for Windows
REM ========================================

echo.
echo ========================================
echo MT5 Sentiment Analysis Bot (Conda)
echo ========================================
echo.

REM Check if conda is installed
where conda >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda from:
    echo   Anaconda: https://www.anaconda.com/products/distribution
    echo   Miniconda: https://docs.conda.io/en/latest/miniconda.html
    echo.
    pause
    exit /b 1
)

echo [OK] Conda found
echo.

REM Check if environment exists
set ENV_NAME=mt5-sentiment-bot
conda env list | findstr /C:"%ENV_NAME%" >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Creating conda environment from environment.yml...
    echo This may take several minutes...
    echo.
    conda env create -f environment.yml
    if errorlevel 1 (
        echo [ERROR] Failed to create conda environment
        pause
        exit /b 1
    )
    echo.
    echo [OK] Conda environment created
) else (
    echo [OK] Conda environment '%ENV_NAME%' already exists
    echo.
    
    REM Ask if user wants to update
    set /p UPDATE="Update environment from environment.yml? (y/n): "
    if /i "%UPDATE%"=="y" (
        echo [SETUP] Updating conda environment...
        conda env update -f environment.yml --prune
        if errorlevel 1 (
            echo [WARNING] Failed to update environment continuing anyway
        ) else (
            echo [OK] Environment updated
        )
    )
)

echo.

REM Activate conda environment
echo [SETUP] Activating conda environment...
call conda activate %ENV_NAME%
if errorlevel 1 (
    echo [ERROR] Failed to activate conda environment
    echo Try running: conda activate %ENV_NAME%
    pause
    exit /b 1
)

echo [OK] Conda environment activated
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

REM Create necessary directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "models" mkdir models
if not exist "reports" mkdir reports

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
