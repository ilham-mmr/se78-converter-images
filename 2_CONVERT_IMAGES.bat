@echo off
cd /d "%~dp0"
title SE78 BMP Converter

echo ============================================
echo SAP SE78 BMP CONVERTER
echo ============================================
echo.
echo This converts supported images in this folder.
echo For automatic sizing, filenames should contain:
echo   HEADER  - 2475 x 300
echo   FOOTER  - 2475 x 150
echo.
echo Examples:
echo   ZKPJ_S050_HEADER.png
echo   ZKPJ_S050_FOOTER.png
echo.
echo --------------------------------------------
echo.

python se78_bmp_converter.py .

if errorlevel 1 (
    echo.
    echo --------------------------------------------
    echo Some files could not be converted.
    echo Read README.md for help.
    echo --------------------------------------------
) else (
    echo.
    echo --------------------------------------------
    echo Conversion completed.
    echo.
    echo Upload files ending in _SE78_256COLOR.BMP
    echo into SAP SE78 - GRAPHICS - BMAP - Color.
    echo --------------------------------------------
)

echo.
pause
