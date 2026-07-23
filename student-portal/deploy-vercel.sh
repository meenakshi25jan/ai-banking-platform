#!/usr/bin/env bash
# Deploy Student Admission Portal to Vercel
# Run from repository root: ./student-portal/deploy-vercel.sh
set -euo pipefail

PORTAL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PORTAL_DIR"

if ! command -v vercel >/dev/null 2>&1; then
  echo "Installing Vercel CLI..."
  npm install -g vercel
fi

echo "==> Deploying from: ${PORTAL_DIR}"
echo "==> IMPORTANT: Vercel Root Directory must be set to 'student-portal'"
echo ""

if [ ! -f .env.local ] && [ -f .env.example ]; then
  cp .env.example .env.local
  echo "Created .env.local — update NEXT_PUBLIC_ODOO_URL before production deploy"
fi

vercel --prod "$@"
