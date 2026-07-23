#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# shellcheck source=lib/common.sh
source "${SCRIPT_DIR}/lib/common.sh"

COMPOSE_FILE="${ROOT_DIR}/deployment/docker-compose.yml"

cd "${ROOT_DIR}"
require_cmd docker

log "Stopping Student Admission ERP stack..."
docker compose -f "${COMPOSE_FILE}" down

log "Stack stopped."
