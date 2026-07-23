#!/usr/bin/env bash
# Push OdooMITNCR to GitHub (run with YOUR GitHub credentials)
set -euo pipefail
cd "$(dirname "$0")/.."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/meenakshi25jan/OdooMITNCR.git
git branch -M main
git push -u origin main
echo "Done: https://github.com/meenakshi25jan/OdooMITNCR"
