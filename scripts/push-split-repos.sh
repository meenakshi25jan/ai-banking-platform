#!/usr/bin/env bash
# Initialize and push split repositories to GitHub
# Usage: ./scripts/push-split-repos.sh YOUR_GITHUB_ORG [--push]
set -euo pipefail

ORG="${1:-}"
DO_PUSH="${2:-}"

if [ -z "$ORG" ]; then
  echo "Usage: $0 <github-org-or-username> [--push]"
  echo "Example: $0 meenakshi25jan --push"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="${ROOT}/student-admission-odoo-backend"
PORTAL="${ROOT}/student-admission-portal-vercel"

setup_repo() {
  local dir="$1"
  local name="$2"
  local msg="$3"
  local url="https://github.com/${ORG}/${name}.git"

  echo ""
  echo "=========================================="
  echo "  ${name}"
  echo "=========================================="

  cd "$dir"

  if [ ! -d .git ]; then
    git init -b main
  fi

  git add .
  if ! git diff --cached --quiet; then
    git commit -m "$msg"
  else
    echo "No changes to commit."
  fi

  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$url"
  else
    git remote add origin "$url"
  fi

  echo "Remote: $url"

  if [ "$DO_PUSH" = "--push" ]; then
    if git ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
      git push -u origin main
      echo "✓ Pushed ${name}"
    else
      echo "✗ Repository not found: $url"
      echo "  Create it first: https://github.com/new?name=${name}&description=Student+Admission+ERP"
      return 1
    fi
  else
    echo "Dry run. Push with: cd $dir && git push -u origin main"
  fi
}

echo "GitHub org/user: ${ORG}"
echo ""
echo "Create empty repos first (no README, no .gitignore):"
echo "  https://github.com/new?name=student-admission-odoo-backend"
echo "  https://github.com/new?name=student-admission-portal-vercel"
echo ""

FAILED=0
setup_repo "$BACKEND" "student-admission-odoo-backend" "Initial commit: Odoo 17 Student Admission ERP backend" || FAILED=1
setup_repo "$PORTAL" "student-admission-portal-vercel" "Initial commit: Next.js Student Admission portal for Vercel" || FAILED=1

if [ "$FAILED" -eq 1 ] && [ "$DO_PUSH" = "--push" ]; then
  echo ""
  echo "Create the missing repos on GitHub, then re-run:"
  echo "  ./scripts/push-split-repos.sh ${ORG} --push"
  exit 1
fi

cat <<EOF

Vercel setup (portal only):
  1. https://vercel.com/new → Import ${ORG}/student-admission-portal-vercel
  2. Framework: Next.js (auto-detected)
  3. Root Directory: . (repo root)
  4. Environment variables:
     NEXT_PUBLIC_ODOO_URL=https://your-odoo-host
     NEXT_PUBLIC_ODOO_DB=student_admission

Odoo backend CORS:
  STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app

EOF
