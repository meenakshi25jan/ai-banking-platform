#!/usr/bin/env bash
set -euo pipefail
SOURCE_REPO="${SOURCE_REPO:-https://github.com/meenakshi25jan/ai-banking-platform}"
SOURCE_BRANCH="${SOURCE_BRANCH:-cursor/odoomitncr-full-app-0cba}"
SOURCE_DIR="${SOURCE_DIR:-OdooMITNCR-publish}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d)
echo "Fetching from ${SOURCE_REPO} (${SOURCE_BRANCH})..."
git clone --depth 1 --branch "$SOURCE_BRANCH" "$SOURCE_REPO" "$TMP/src"
SRC_PATH="$TMP/src/$SOURCE_DIR"
[ -d "$SRC_PATH" ] || SRC_PATH="$TMP/src/OdooMITNCR"
[ -d "$SRC_PATH" ] || { echo "Bundle not found"; exit 1; }
shopt -s dotglob
for item in "$SRC_PATH"/*; do
  name=$(basename "$item")
  [ "$name" = ".git" ] && continue
  cp -a "$item" "$ROOT/"
done
chmod +x "$ROOT"/scripts/*.sh 2>/dev/null || true
rm -rf "$TMP"
echo "Import complete. Run: ./scripts/push-to-github.sh"
