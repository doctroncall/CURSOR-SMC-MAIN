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
REM Locate conda installation
set "CONDA_BAT="
if exist "%USERPROFILE%\anaconda3\Scripts\conda.exe" (
    set "CONDA_BAT=%USERPROFILE%\anaconda3\Scripts\activate.bat"
) else if exist "%USERPROFILE%\miniconda3\Scripts\conda.exe" (
    set "CONDA_BAT=%USERPROFILE%\miniconda3\Scripts\activate.bat"
) else if exist "%ProgramData%\anaconda3\Scripts\conda.exe" (
    set "CONDA_BAT=%ProgramData%\anaconda3\Scripts\activate.bat"
) else if exist "%ProgramData%\miniconda3\Scripts\conda.exe" (
    set "CONDA_BAT=%ProgramData%\miniconda3\Scripts\activate.bat"
)

REM Try to find conda via conda info
if "%CONDA_BAT%"=="" (
    for /f "tokens=*" %%i in ('conda info --base 2^>nul') do (
        if exist "%%i\Scripts\activate.bat" set "CONDA_BAT=%%i\Scripts\activate.bat"
    )
)

if "%CONDA_BAT%"=="" (
    echo [ERROR] Could not locate conda activate.bat
    echo Please ensure Anaconda/Miniconda is properly installed
    echo.
    echo Try running: conda init cmd.exe
    echo Then close and reopen this terminal
    pause
    exit /b 1
)

echo [OK] Found conda activation script: %CONDA_BAT%
echo.

REM Check if conda environment exists
echo [SETUP] Checking for conda environment 'mt5-sentiment-bot'...
conda env list | findstr /C:"mt5-sentiment-bot" >nul 2>&1
if errorlevel 1 (
    echo [SETUP] Environment not found - creating from environment.yml...
    echo This will take 5-15 minutes - please be patient
    echo.
    
    REM Check if environment.yml exists
    if not exist "environment.yml" (
        echo [ERROR] environment.yml not found in current directory
        echo Current directory: %CD%
        echo Please ensure environment.yml is in the project directory
        pause
        exit /b 1
    )
    
    echo [SETUP] Installing packages with conda...
    echo Progress: This includes TA-Lib and all ML libraries
    echo.
    echo Running: conda env create -f environment.yml
    echo.
    conda env create -f environment.yml --yes
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create conda environment
        echo.
        echo Troubleshooting:
        echo 1. Check your internet connection
        echo 2. Try: conda clean --all
        echo 3. Try: conda update conda
        echo 4. Check the error messages above
        echo 5. Try manually: conda env create -f environment.yml
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Conda environment 'mt5-sentiment-bot' created successfully
    echo.
) else (
    echo [OK] Conda environment 'mt5-sentiment-bot' already exists
    echo [INFO] To update: conda env update -f environment.yml --prune
    echo.
)

echo.
echo [SETUP] Activating conda environment...

REM Activate the conda environment using the activate.bat script
call "%CONDA_BAT%" mt5-sentiment-bot
if errorlevel 1 (
    echo [ERROR] Failed to activate conda environment
    echo.
    echo Try these solutions:
    echo 1. Close and reopen your terminal
    echo 2. Run: conda init cmd.exe
    echo 3. Delete and recreate environment: conda env remove -n mt5-sentiment-bot
    echo 4. Manually run: %CONDA_BAT% mt5-sentiment-bot
    echo.
    pause
    exit /b 1
)

echo [OK] Conda environment activated: mt5-sentiment-bot
echo Python: 
python --version
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
