@echo off
title Language Buddy Launcher
echo.
echo 🌍 Starting Language Buddy...
echo.
echo If this is your first time running the app, please wait while we install required packages...
echo.

REM Install requirements first
pip install -r requirements.txt

REM Clear screen and start the app
cls
echo.
echo 🌍 Language Buddy is starting...
echo.
python language_buddy.py

echo.
echo Language Buddy has closed. Press any key to exit...
pause > nul
