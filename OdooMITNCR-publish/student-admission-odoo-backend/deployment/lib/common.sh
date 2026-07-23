#!/usr/bin/env bash
# Shared helpers for deployment scripts

log() { echo "==> $*"; }
err() { echo "ERROR: $*" >&2; }

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    err "Required command not found: $1"
    exit 1
  fi
}

repo_root() {
  cd "$(dirname "${BASH_SOURCE[1]}")/.." && pwd
}

wait_for_url() {
  local url="$1"
  local label="${2:-service}"
  local max_wait="${3:-180}"
  local elapsed=0

  log "Waiting for ${label} at ${url}..."
  while [ "$elapsed" -lt "$max_wait" ]; do
    if curl -sf "$url" >/dev/null 2>&1; then
      log "${label} is ready."
      return 0
    fi
    sleep 3
    elapsed=$((elapsed + 3))
  done

  err "${label} did not become ready within ${max_wait}s (${url})"
  return 1
}

ensure_env_file() {
  local root="$1"
  if [ ! -f "${root}/.env" ]; then
    log "Creating .env from .env.example"
    cp "${root}/.env.example" "${root}/.env"
  fi
}
