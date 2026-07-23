#!/usr/bin/env bash
set -euo pipefail

PORTAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../student-portal" && pwd)"
cd "$PORTAL_DIR"

if [ ! -f .env.local ]; then
  cp .env.example .env.local
  echo "Created .env.local from .env.example"
fi

npm install
npm run dev
