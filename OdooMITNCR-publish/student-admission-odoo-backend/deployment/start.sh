#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

source "${SCRIPT_DIR}/lib/common.sh"

log "Student Admission Odoo Backend — Startup"
log "Repository root: ${ROOT_DIR}"

require_cmd docker

if ! docker compose version >/dev/null 2>&1; then
  err "Docker Compose v2 is required (docker compose)."
  exit 1
fi

ensure_env_file "${ROOT_DIR}"

cd "${ROOT_DIR}"

log "Building and starting PostgreSQL + Odoo..."
docker compose up -d --build

log "Waiting for Odoo initialization (first run may take 3-5 minutes)..."
if wait_for_url "http://localhost:8069/api/health" "Odoo" 300; then
  curl -sf "http://localhost:8069/api/health" && echo ""
else
  err "Odoo failed to start. Check logs: docker compose logs odoo"
  exit 1
fi

cat <<EOF

============================================
  Odoo Backend Ready
============================================
  URL:           http://localhost:8069
  Database:      student_admission
  Admin login:   admin / admin
  PostgreSQL:    localhost:5433
  Health:        http://localhost:8069/api/health
  API:           http://localhost:8069/api/v1/courses

  Connect portal with:
    NEXT_PUBLIC_ODOO_URL=http://localhost:8069
============================================

EOF
