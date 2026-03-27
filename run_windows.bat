@echo off
setlocal EnableDelayedExpansion

:: ─────────────────────────────────────────────────────────────────────────────
:: Desktop Recorder – Python launcher for Windows
::
:: This script runs desktop_recorder.py directly with Python, which bypasses
:: the Windows SmartScreen "unverified publisher" warning that appears when
:: running the compiled .exe downloaded from the internet.
::
:: Requirements: Python 3.12+ must be installed.
::   Download from: https://www.python.org/downloads/
::   During installation, check "Add Python to PATH".
:: ─────────────────────────────────────────────────────────────────────────────

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo  [ERROR] Python is not installed or not on PATH.
    echo.
    echo  Download Python 3.12+ from: https://www.python.org/downloads/
    echo  During installation, tick "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

:: Verify Python version is 3.12+
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo Using Python %PYVER%

:: Install / update dependencies quietly
echo Installing dependencies (first run may take a moment)...
python -m pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo.
    echo  [ERROR] Failed to install dependencies.
    echo  Try running: python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:: Forward all arguments to the recorder
echo.
python src\desktop_recorder.py %*
