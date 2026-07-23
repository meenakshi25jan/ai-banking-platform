#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

source "${SCRIPT_DIR}/lib/common.sh"

cd "${ROOT_DIR}"
require_cmd docker

log "Stopping Odoo backend stack..."
docker compose down

log "Stack stopped."
