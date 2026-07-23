#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PORTAL_DIR="${ROOT_DIR}/student-portal"
PORTAL_URL="http://localhost:3000"
MODE="${1:-local}"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"

COMPOSE_FILE="${ROOT_DIR}/deployment/docker-compose.yml"

start_portal_docker() {
  require_cmd docker
  ensure_env_file "${ROOT_DIR}"
  cd "${ROOT_DIR}"

  log "Starting portal via Docker..."
  docker compose -f "${COMPOSE_FILE}" up -d --build portal

  if wait_for_url "${PORTAL_URL}/api/health" "Portal (Docker)" 120; then
    curl -sf "${PORTAL_URL}/api/health" && echo ""
    print_success_docker
  else
    err "Portal container failed. Logs: docker compose -f deployment/docker-compose.yml logs portal"
    exit 1
  fi
}

start_portal_local() {
  require_cmd node
  require_cmd npm

  if ! curl -sf "http://localhost:8069/api/health" >/dev/null 2>&1; then
    log "Odoo is not running on :8069 — starting backend first..."
    "${SCRIPT_DIR}/start.sh"
  fi

  cd "${PORTAL_DIR}"

  if [ ! -f .env.local ]; then
    log "Creating student-portal/.env.local from .env.example"
    cp .env.example .env.local
  fi

  log "Installing npm dependencies..."
  npm install

  log "Starting Next.js development server on port 3000..."
  npm run dev &
  PORTAL_PID=$!

  cleanup() {
    log "Stopping portal (pid ${PORTAL_PID})..."
    kill "${PORTAL_PID}" 2>/dev/null || true
  }
  trap cleanup EXIT INT TERM

  if wait_for_url "${PORTAL_URL}/api/health" "Portal (local)" 90; then
    curl -sf "${PORTAL_URL}/api/health" && echo ""
    print_success_local "${PORTAL_PID}"
    wait "${PORTAL_PID}"
  else
    err "Portal failed to start. Check output above."
    exit 1
  fi
}

print_success_docker() {
  cat <<EOF

============================================
  Portal Ready (Docker)
============================================
  Portal URL:    ${PORTAL_URL}
  Health check:  ${PORTAL_URL}/api/health
  Odoo API:      http://localhost:8069/api/v1/courses
============================================

EOF
}

print_success_local() {
  cat <<EOF

============================================
  Portal Ready (Local Dev)
============================================
  Portal URL:    ${PORTAL_URL}
  Health check:  ${PORTAL_URL}/api/health
  Odoo API:      http://localhost:8069/api/v1/courses
  Process PID:   $1
  Press Ctrl+C to stop.
============================================

EOF
}

case "${MODE}" in
  docker|--docker)
    start_portal_docker
    ;;
  local|--local|"")
    start_portal_local
    ;;
  *)
    err "Unknown mode: ${MODE}. Use: local | docker"
    exit 1
    ;;
esac
