#!/usr/bin/env bash
# Initialize and push split repositories to GitHub
# Usage: ./scripts/push-split-repos.sh YOUR_GITHUB_ORG
set -euo pipefail

ORG="${1:-}"
if [ -z "$ORG" ]; then
  echo "Usage: $0 <github-org-or-username>"
  echo "Example: $0 meenakshi25jan"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="${ROOT}/student-admission-odoo-backend"
PORTAL="${ROOT}/student-admission-portal-vercel"

push_repo() {
  local dir="$1"
  local name="$2"
  local msg="$3"

  echo ""
  echo "=========================================="
  echo "  Setting up: $name"
  echo "=========================================="

  cd "$dir"

  if [ ! -d .git ]; then
    git init
    git checkout -b main 2>/dev/null || git branch -M main
  fi

  git add .
  git diff --cached --quiet && echo "No changes to commit in $name" || git commit -m "$msg"

  if git remote get-url origin >/dev/null 2>&1; then
    echo "Remote origin already set"
  else
    git remote add origin "git@github.com:${ORG}/${name}.git"
  fi

  echo "Ready to push: git@github.com:${ORG}/${name}.git"
  echo "Run manually after creating the repo on GitHub:"
  echo "  cd $dir && git push -u origin main"
}

push_repo "$BACKEND" "student-admission-odoo-backend" "Initial commit: Odoo 17 Student Admission ERP backend"
push_repo "$PORTAL" "student-admission-portal-vercel" "Initial commit: Next.js Student Admission portal for Vercel"

cat <<EOF

Next steps:
1. Create empty repos on GitHub:
   - https://github.com/new → student-admission-odoo-backend
   - https://github.com/new → student-admission-portal-vercel

2. Push each repo:
   cd student-admission-odoo-backend && git push -u origin main
   cd student-admission-portal-vercel && git push -u origin main

3. Import student-admission-portal-vercel in Vercel (NOT the monorepo)

4. Set Vercel env vars:
   NEXT_PUBLIC_ODOO_URL=https://your-odoo-backend-url
   NEXT_PUBLIC_ODOO_DB=student_admission

EOF
