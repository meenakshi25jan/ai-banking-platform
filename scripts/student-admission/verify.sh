#!/usr/bin/env bash
# Verify all services are healthy
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

log "Checking services..."

check() {
  local name="$1" url="$2"
  if curl -sf "$url" >/dev/null 2>&1; then
    ok "$name — $url"
  else
    err "$name — NOT RUNNING ($url)"
    return 1
  fi
}

FAIL=0
check "Odoo health" "http://localhost:8069/api/health" || FAIL=1
check "Portal health" "http://localhost:3000/api/health" || FAIL=1

if [ "$FAIL" -eq 0 ]; then
  ok "All services healthy"
else
  err "Some services are down. Run start-all.sh"
  exit 1
fi
