@echo off
REM ========================================
REM MT5 Sentiment Analysis Bot Launcher
REM Anaconda/Conda Version
REM ========================================
REM This script uses Anaconda for better stability with ML dependencies

setlocal enabledelayedexpansion

echo.
echo ========================================
echo MT5 Sentiment Analysis Bot (Anaconda)
echo ========================================
echo.

REM Check if conda is installed
where conda >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Anaconda/Miniconda is not installed or not in PATH
    echo.
    echo Please install Anaconda or Miniconda:
    echo   - Anaconda (full): https://www.anaconda.com/download
    echo   - Miniconda (minimal): https://docs.conda.io/en/latest/miniconda.html
    echo.
    echo After installation:
    echo   1. Restart your command prompt
    echo   2. Run this script again
    echo.
    pause
    exit /b 1
)

REM Get conda version
set CONDA_VERSION=unknown
for /f "tokens=2" %%i in ('conda --version 2^>^&1') do set CONDA_VERSION=%%i
echo [OK] Conda found - Version %CONDA_VERSION%
echo.

REM Initialize conda for batch script
call conda info --envs >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Initializing conda for cmd.exe...
    call conda init cmd.exe
    echo [INFO] Please close and reopen this terminal, then run this script again
    pause
    exit /b 0
)

REM Check if conda environment exists
conda env list | findstr "mt5-sentiment-bot" >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Creating conda environment from environment.yml...
    echo This will take 5-15 minutes - please be patient
    echo.
    
    REM Check if environment.yml exists
    if not exist "environment.yml" (
        echo [ERROR] environment.yml not found
        echo Please ensure environment.yml is in the project directory
        pause
        exit /b 1
    )
    
    echo [SETUP] Installing packages with conda...
    echo Progress: This includes TA-Lib and all ML libraries
    echo.
    conda env create -f environment.yml
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create conda environment
        echo.
        echo Troubleshooting:
        echo 1. Check your internet connection
        echo 2. Try: conda clean --all
        echo 3. Try: conda update conda
        echo 4. Check the error messages above
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Conda environment created successfully
    echo.
) else (
    echo [OK] Conda environment 'mt5-sentiment-bot' already exists
    echo [INFO] To update environment: conda env update -f environment.yml
)

echo.
echo [SETUP] Activating conda environment...

REM Activate the conda environment
call conda activate mt5-sentiment-bot
if errorlevel 1 (
    echo [ERROR] Failed to activate conda environment
    echo.
    echo Try these solutions:
    echo 1. Close and reopen your terminal
    echo 2. Run: conda init cmd.exe
    echo 3. Delete and recreate environment: conda env remove -n mt5-sentiment-bot
    echo.
    pause
    exit /b 1
)

echo [OK] Conda environment activated
echo Environment: mt5-sentiment-bot
echo.

REM Verify key packages are installed
echo [SETUP] Verifying installation...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Streamlit not found, attempting to install missing packages...
    conda env update -f environment.yml
)

python -c "import talib" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] TA-Lib not properly installed
    echo Attempting to install from conda-forge...
    conda install -c conda-forge ta-lib -y
    if errorlevel 1 (
        echo [ERROR] TA-Lib installation failed
        echo Try manually: conda install -c conda-forge ta-lib
        pause
        exit /b 1
    )
)

echo [OK] All packages verified
echo.

REM Create necessary directories
echo [SETUP] Checking directory structure...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "models" mkdir models
if not exist "reports" mkdir reports
echo [OK] Directory structure ready
echo.

REM Check if database needs initialization
if not exist "data\mt5_sentiment.db" (
    echo [SETUP] Initializing database...
    python -c "from src.database.models import init_database; init_database(); print('[OK] Database initialized')" 2>nul
    if errorlevel 1 (
        echo [WARNING] Database initialization failed - will retry on first run
        echo This is normal for first-time setup
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
echo [INFO] Using Anaconda environment: mt5-sentiment-bot
echo [INFO] Dashboard will open in your browser automatically
echo [INFO] Press Ctrl+C to stop the bot
echo.
echo Launching Streamlit...
echo.

REM Start Streamlit with the app
set STREAMLIT_EXIT_CODE=0
streamlit run app.py --server.headless=true --server.port=8501
set STREAMLIT_EXIT_CODE=%errorlevel%

REM If Streamlit exits, show message
echo.
echo ========================================
echo Bot stopped
echo ========================================

if "%STREAMLIT_EXIT_CODE%" NEQ "0" (
    echo.
    echo [WARNING] Application exited with error code: %STREAMLIT_EXIT_CODE%
    echo Check the logs folder for error details
    echo.
)

echo.
echo To restart the bot, run this script again.
echo To deactivate conda: conda deactivate
echo.
pause

endlocal
