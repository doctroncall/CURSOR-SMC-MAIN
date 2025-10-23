@echo off
REM ========================================
REM Quick Fix for Missing loguru Module
REM ========================================

echo.
echo ========================================
echo   FIXING MISSING LOGURU MODULE
echo ========================================
echo.

REM Try to find conda
where conda >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Conda not found in PATH
    echo.
    echo Please run this script from Anaconda Prompt
    echo Or manually run: conda install -c conda-forge loguru
    echo.
    pause
    exit /b 1
)

echo [OK] Conda found
echo.

REM Check which environment is active
echo [INFO] Checking active environment...
echo Current environment: %CONDA_DEFAULT_ENV%
echo.

REM Install loguru
echo [1/2] Installing loguru...
echo.
conda install -c conda-forge loguru -y
if errorlevel 1 (
    echo [ERROR] Failed to install loguru with conda
    echo [INFO] Trying with pip...
    pip install loguru
    if errorlevel 1 (
        echo [ERROR] Failed to install loguru
        echo.
        echo Please try manually:
        echo   conda activate smc_bot
        echo   conda install -c conda-forge loguru
        echo.
        pause
        exit /b 1
    )
)

echo [OK] loguru installed successfully
echo.

REM Verify installation
echo [2/2] Verifying installation...
python -c "import loguru; print('[OK] loguru version:', loguru.__version__)" 2>nul
if errorlevel 1 (
    echo [WARNING] Could not verify loguru installation
    echo Please check if it's working:
    echo   python -c "import loguru; print(loguru.__version__)"
) else (
    echo [OK] loguru is working correctly
)

echo.
echo ========================================
echo   FIX COMPLETE!
echo ========================================
echo.
echo You can now run "conda smc.bat" to start the bot
echo.
pause
