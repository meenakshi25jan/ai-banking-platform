@echo off
setlocal EnableExtensions
REM Student Admission ERP — Windows setup
cd /d "%~dp0..\.."
set "ROOT=%CD%"

echo ============================================
echo   Student Admission ERP - Setup (Windows)
echo ============================================
echo Repo: %ROOT%

where node >nul 2>&1 || (echo ERROR: Node.js required. Install from https://nodejs.org & exit /b 1)
where npm >nul 2>&1 || (echo ERROR: npm required & exit /b 1)

if exist "%ROOT%\student-admission-odoo-backend\.env.example" (
  if not exist "%ROOT%\student-admission-odoo-backend\.env" (
    copy "%ROOT%\student-admission-odoo-backend\.env.example" "%ROOT%\student-admission-odoo-backend\.env" >nul
  )
  echo [OK] Odoo .env ready
)

if exist "%ROOT%\student-admission-portal-vercel" (
  if not exist "%ROOT%\student-admission-portal-vercel\.env.local" (
    copy "%ROOT%\student-admission-portal-vercel\.env.example" "%ROOT%\student-admission-portal-vercel\.env.local" >nul
  )
  echo Installing portal dependencies...
  pushd "%ROOT%\student-admission-portal-vercel"
  call npm install
  popd
  echo [OK] Portal ready
)

echo.
echo Setup complete!
echo   run setup.bat once, then:
echo   start-odoo.bat    - Odoo backend (Docker)
echo   start-portal.bat  - Next.js portal
echo.
pause
