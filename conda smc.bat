@echo off
REM =============================================
REM SMC Bot - Main Orchestrator
REM Simple and Direct - Anaconda Environment
REM =============================================

echo.
echo =============================================
echo      SMC BOT - ANACONDA LAUNCHER
echo =============================================
echo.

REM Step 1: Check if conda is installed
echo [1/5] Checking Conda installation...
where conda >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Conda not found!
    echo.
    echo Please install Anaconda or Miniconda from:
    echo   https://www.anaconda.com/download
    echo.
    pause
    exit /b 1
)
echo [OK] Conda is installed
echo.

REM Step 2: Check if environment exists, create if needed
echo [2/5] Checking conda environment "smc bot"...
conda env list | findstr /C:"smc bot" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Environment "smc bot" not found - creating now...
    echo [INFO] This will take a few minutes...
    echo.
    
    if not exist "environment.yml" (
        echo [ERROR] environment.yml not found!
        echo Please ensure you're in the bot directory
        pause
        exit /b 1
    )
    
    REM Create environment with custom name
    conda env create -f environment.yml -n "smc bot"
    if errorlevel 1 (
        echo [ERROR] Failed to create environment!
        echo Try: conda clean --all
        echo Then run this script again
        pause
        exit /b 1
    )
    echo [OK] Environment created successfully
) else (
    echo [OK] Environment "smc bot" already exists
)
echo.

REM Step 3: Activate the environment
echo [3/5] Activating conda environment...
call conda activate "smc bot"
if errorlevel 1 (
    echo [ERROR] Failed to activate environment!
    echo Try: conda init cmd.exe
    echo Then restart your terminal and try again
    pause
    exit /b 1
)
echo [OK] Environment activated
echo.

REM Step 4: Verify and install dependencies
echo [4/5] Verifying dependencies...

REM Check critical packages
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing missing packages...
    conda env update -f environment.yml -n "smc bot"
)

python -c "import talib" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing TA-Lib...
    conda install -c conda-forge ta-lib -y
)

python -c "import MetaTrader5" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing MetaTrader5...
    pip install MetaTrader5
)

echo [OK] All dependencies ready
echo.

REM Create necessary directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "models" mkdir models
if not exist "reports" mkdir reports

REM Step 5: Launch the bot
echo [5/5] Launching SMC Bot...
echo.
echo =============================================
echo      BOT IS STARTING
echo =============================================
echo.
echo The dashboard will open in your browser
echo Press Ctrl+C to stop the bot
echo.

streamlit run app.py --server.headless=true --server.port=8501

REM When bot stops
echo.
echo =============================================
echo      BOT STOPPED
echo =============================================
echo.
echo To restart: Run "conda smc.bat" again
echo.
pause
