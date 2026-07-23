#!/usr/bin/env bash
# Stop Odoo + PostgreSQL Docker stack
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(find_repo_root)"
ODOO="$ROOT/student-admission-odoo-backend"

log "Stopping Odoo backend..."
cd "$ODOO"
docker compose down
ok "Odoo stopped"
