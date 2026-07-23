#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== OdooMITNCR Codespace Setup ==="
cd student-admission-portal-vercel && cp -n .env.example .env.local 2>/dev/null || true && npm install && cd "$ROOT"
cd server && cp -n .env.example .env 2>/dev/null || true && npm install && cd "$ROOT"
cd student-admission-odoo-backend && cp -n .env.example .env 2>/dev/null || true && cd "$ROOT"
cd student-admission-portal-vercel && npm run build && cd "$ROOT"
echo "Setup complete. Run: npm run odoo:up && npm run dev:portal"
