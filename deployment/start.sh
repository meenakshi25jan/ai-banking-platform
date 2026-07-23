#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> Starting Student Admission ERP (Odoo + PostgreSQL)..."
docker compose up -d --build

echo ""
echo "==> Waiting for Odoo to be ready..."
sleep 15

echo ""
echo "============================================"
echo "  Odoo Backend:  http://localhost:8069"
echo "  Database:      student_admission"
echo "  Admin login:   admin / admin"
echo "  PostgreSQL:    localhost:5433"
echo "============================================"
echo ""
echo "Next: Start the portal with:"
echo "  cd student-portal && npm install && npm run dev"
