@echo off
setlocal EnableExtensions
cd /d "%~dp0..\.."
set "ROOT=%CD%"
set "ODOO=%ROOT%\student-admission-odoo-backend"

echo ============================================
echo   Starting Odoo Backend (Docker)
echo ============================================

where docker >nul 2>&1 || (echo ERROR: Docker Desktop required. Install from https://docker.com & pause & exit /b 1)

if not exist "%ODOO%\.env" (
  copy "%ODOO%\.env.example" "%ODOO%\.env" >nul
)

pushd "%ODOO%"
docker compose up -d --build
if errorlevel 1 (
  echo ERROR: docker compose failed
  popd
  pause
  exit /b 1
)
popd

echo.
echo Waiting for Odoo (first run: 3-5 minutes)...
set /a COUNT=0
:WAIT_ODOO
curl -sf http://localhost:8069/api/health >nul 2>&1 && goto ODOO_READY
timeout /t 5 /nobreak >nul
set /a COUNT+=5
if %COUNT% GEQ 300 (
  echo ERROR: Odoo did not start. Run: docker compose logs odoo
  pause
  exit /b 1
)
goto WAIT_ODOO

:ODOO_READY
echo.
echo ============================================
echo   Odoo Backend Ready
echo ============================================
echo   URL:      http://localhost:8069
echo   Login:    admin / admin
echo   Database: student_admission
echo ============================================
echo.
pause
