#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"

log "Student Admission ERP — Backend Startup"
log "Repository root: ${ROOT_DIR}"

require_cmd docker

if ! docker compose version >/dev/null 2>&1; then
  err "Docker Compose v2 is required (docker compose)."
  exit 1
fi

ensure_env_file "${ROOT_DIR}"

cd "${ROOT_DIR}"

COMPOSE_FILE="${ROOT_DIR}/deployment/docker-compose.yml"

log "Building and starting PostgreSQL + Odoo..."
docker compose -f "${COMPOSE_FILE}" up -d --build db odoo

log "Waiting for Odoo initialization (first run may take 3-5 minutes)..."
if wait_for_url "http://localhost:8069/api/health" "Odoo" 300; then
  HEALTH_JSON=$(curl -sf "http://localhost:8069/api/health" || echo '{}')
  log "Odoo health: ${HEALTH_JSON}"
else
  err "Odoo failed to start. Check logs: docker compose -f deployment/docker-compose.yml logs odoo"
  exit 1
fi

cat <<EOF

============================================
  Student Admission ERP — Backend Ready
============================================
  Odoo URL:      http://localhost:8069
  Database:      student_admission
  Admin login:   admin / admin
  PostgreSQL:    localhost:5433
  Health check:  http://localhost:8069/api/health

  Demo users:
    admission.officer@institute.edu / demo123
    accounts@institute.edu / demo123
    rahul.sharma@example.com / demo123

  Next step — start the portal:
    chmod +x deployment/start-portal.sh
    ./deployment/start-portal.sh

  Or start everything with Docker:
    docker compose -f deployment/docker-compose.yml up -d
============================================

EOF
