@echo off
setlocal
REM Delegate to the robust conda launcher (handles env creation and dependencies)
call "conda smc.bat"
endlocal
