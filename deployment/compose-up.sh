#!/usr/bin/env bash
# Convenience wrapper: start full Student Admission ERP stack
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
[ -f .env ] || cp deployment/.env.example .env
exec docker compose -f deployment/docker-compose.yml up -d --build "$@"
