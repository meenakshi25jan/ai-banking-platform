#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v vercel >/dev/null 2>&1; then
  npm install -g vercel
fi
[ -f .env.local ] || cp .env.example .env.local
vercel --prod "$@"
