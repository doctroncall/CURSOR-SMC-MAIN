@echo off
REM ========================================
REM Dependency Verification Script
REM ========================================

echo.
echo Running dependency verification...
echo.

REM Check if Python is available
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please activate your conda environment first:
    echo   conda activate smc_bot
    echo.
    pause
    exit /b 1
)

REM Run the verification script
python verify_dependencies.py

REM Exit code is passed from Python script
exit /b %errorlevel%
