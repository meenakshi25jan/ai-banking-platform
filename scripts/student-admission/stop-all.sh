#!/usr/bin/env bash
# Stop Odoo Docker stack (portal: Ctrl+C if running in terminal)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/stop-odoo.sh"
echo "If portal is running, stop it with Ctrl+C in that terminal."
