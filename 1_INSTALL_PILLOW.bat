@echo off
cd /d "%~dp0"
title SE78 BMP Converter - Install Pillow
echo ============================================
echo SE78 BMP CONVERTER - FIRST TIME SETUP
echo ============================================
echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python was not found.
    echo.
    echo Install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo During installation, enable: Add Python to PATH
    echo.
    pause
    exit /b 1
)

echo.
echo Installing Pillow...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Installation failed.
    echo Check your internet connection and Python installation.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Pillow installed successfully.
echo You can now use 2_CONVERT_IMAGES.bat
echo ============================================
echo.
pause
