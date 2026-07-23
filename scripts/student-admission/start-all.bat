@echo off
setlocal EnableExtensions
REM Start Odoo then Portal (two windows)
cd /d "%~dp0"

echo Starting Odoo in new window...
start "Odoo Backend" cmd /k "%~dp0start-odoo.bat"

echo Waiting 30 seconds for Odoo to initialize...
timeout /t 30 /nobreak >nul

echo Starting Portal in new window...
start "Student Portal" cmd /k "%~dp0start-portal.bat"

echo.
echo ============================================
echo   Services starting in separate windows
echo ============================================
echo   Odoo:    http://localhost:8069
echo   Portal:  http://localhost:3000
echo ============================================
pause
