@echo off
setlocal EnableExtensions
cd /d "%~dp0..\.."
set "ODOO=%CD%\student-admission-odoo-backend"

echo Stopping Odoo Docker stack...
pushd "%ODOO%"
docker compose down
popd
echo [OK] Odoo stopped
pause
