#!/usr/bin/env bash
# Start Odoo 17 + PostgreSQL (Docker)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(find_repo_root)"
ODOO="$ROOT/student-admission-odoo-backend"

require_cmd docker

if ! docker compose version >/dev/null 2>&1; then
  err "Docker Compose v2 required. Install Docker Desktop."
  exit 1
fi

[ -f "$ODOO/.env" ] || cp "$ODOO/.env.example" "$ODOO/.env"

log "Starting Odoo backend (first run: 3-5 minutes)..."
cd "$ODOO"
docker compose up -d --build

wait_for_url "http://localhost:8069/api/health" "Odoo" 300

cat <<EOF

============================================
  Odoo Backend Ready
============================================
  URL:         http://localhost:8069
  Database:    student_admission
  Login:       admin / admin
  Health:      http://localhost:8069/api/health
  API:         http://localhost:8069/api/v1/courses
============================================

EOF
