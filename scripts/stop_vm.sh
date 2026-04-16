#!/usr/bin/env bash
set -euo pipefail
for session in backend ai frontend; do
  if tmux has-session -t "$session" 2>/dev/null; then
    tmux kill-session -t "$session"
    echo "Stopped $session"
  else
    echo "No tmux session named $session"
  fi
done
