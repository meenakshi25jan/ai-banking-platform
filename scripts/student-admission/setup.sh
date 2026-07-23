#!/usr/bin/env bash
# First-time setup — env files + npm install
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(find_repo_root)"
ODOO="$ROOT/student-admission-odoo-backend"
PORTAL="$ROOT/student-admission-portal-vercel"
SERVER="$ROOT/server"

log "Student Admission ERP — Setup"
log "Repo root: $ROOT"

require_cmd node
require_cmd npm

# Odoo env
if [ -d "$ODOO" ]; then
  [ -f "$ODOO/.env" ] || cp "$ODOO/.env.example" "$ODOO/.env"
  ok "Odoo .env ready"
fi

# Portal env + deps
if [ -d "$PORTAL" ]; then
  [ -f "$PORTAL/.env.local" ] || cp "$PORTAL/.env.example" "$PORTAL/.env.local"
  log "Installing portal dependencies..."
  (cd "$PORTAL" && npm install)
  ok "Portal dependencies installed"
fi

# Banking API (optional)
if [ -d "$SERVER" ]; then
  [ -f "$SERVER/.env" ] || cp "$SERVER/.env.example" "$SERVER/.env"
  log "Installing server dependencies..."
  (cd "$SERVER" && npm install)
  ok "Server dependencies installed"
fi

cat <<EOF

Setup complete!

Next steps:
  ./scripts/student-admission/start-all.sh     # Odoo + Portal
  ./scripts/student-admission/start-odoo.sh    # Odoo only
  ./scripts/student-admission/start-portal.sh  # Portal only

EOF
