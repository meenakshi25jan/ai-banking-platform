#!/usr/bin/env bash
# Start Odoo backend + Next.js portal (portal in foreground)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

log() { echo "[$(date +%H:%M:%S)] $*"; }

log "=== Student Admission ERP — Start All ==="

# Start Odoo in background via start-odoo.sh
"$SCRIPT_DIR/start-odoo.sh"

PORTAL_PID=""
cleanup() {
  log "Stopping portal..."
  [ -n "$PORTAL_PID" ] && kill "$PORTAL_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

log "Starting portal in background..."
"$SCRIPT_DIR/start-portal.sh" &
PORTAL_PID=$!

sleep 5

cat <<EOF

============================================
  All services running
============================================
  Portal:  http://localhost:3000
  Odoo:    http://localhost:8069  (admin / admin)
  Health:  http://localhost:3000/api/health

  Press Ctrl+C to stop portal.
  Stop Odoo: ./scripts/student-admission/stop-odoo.sh
============================================

EOF

wait "$PORTAL_PID"
