@echo off
setlocal EnableExtensions
cd /d "%~dp0..\.."
set "ROOT=%CD%"
set "PORTAL=%ROOT%\student-admission-portal-vercel"

echo ============================================
echo   Starting Next.js Portal
echo ============================================

where node >nul 2>&1 || (echo ERROR: Node.js required & pause & exit /b 1)

if not exist "%PORTAL%\.env.local" (
  copy "%PORTAL%\.env.example" "%PORTAL%\.env.local" >nul
)

if not exist "%PORTAL%\node_modules" (
  echo Installing dependencies...
  pushd "%PORTAL%"
  call npm install
  popd
)

echo Portal: http://localhost:3000
echo Press Ctrl+C to stop
echo.
pushd "%PORTAL%"
call npm run dev
popd
