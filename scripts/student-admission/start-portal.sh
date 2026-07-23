#!/usr/bin/env bash
# Start Next.js Student Admission Portal
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(find_repo_root)"
PORTAL="$ROOT/student-admission-portal-vercel"

require_cmd node
require_cmd npm

[ -f "$PORTAL/.env.local" ] || cp "$PORTAL/.env.example" "$PORTAL/.env.local"

if [ ! -d "$PORTAL/node_modules" ]; then
  log "Installing portal dependencies..."
  (cd "$PORTAL" && npm install)
fi

log "Starting Next.js portal on http://localhost:3000"
cd "$PORTAL"
npm run dev
