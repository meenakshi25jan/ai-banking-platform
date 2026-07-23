@echo off
setlocal EnableExtensions
echo Checking services...
curl -sf http://localhost:8069/api/health >nul 2>&1 && echo [OK] Odoo  http://localhost:8069 || echo [FAIL] Odoo not running
curl -sf http://localhost:3000/api/health >nul 2>&1 && echo [OK] Portal http://localhost:3000 || echo [FAIL] Portal not running
pause
