#!/usr/bin/env bash
# Shared helpers for Student Admission run scripts
set -euo pipefail

find_repo_root() {
  local lib_dir
  lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local dir
  dir="$(cd "$lib_dir/../../.." && pwd)"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/student-admission-odoo-backend" ] && [ -d "$dir/student-admission-portal-vercel" ]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo "ERROR: Could not find repo root (need student-admission-odoo-backend + student-admission-portal-vercel)" >&2
  return 1
}

log() { echo "[$(date +%H:%M:%S)] $*"; }
ok()  { echo "✓ $*"; }
err() { echo "ERROR: $*" >&2; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { err "'$1' is required but not installed."; exit 1; }
}

wait_for_url() {
  local url="$1" name="$2" max="${3:-120}" i=0
  while [ $i -lt "$max" ]; do
    if curl -sf "$url" >/dev/null 2>&1; then
      ok "$name is ready: $url"
      return 0
    fi
    sleep 2
    i=$((i + 2))
  done
  err "$name did not become ready at $url"
  return 1
}
