#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_DIR="$ROOT_DIR/server"
AI_DIR="$ROOT_DIR/ai-service"
CLIENT_DIR="$ROOT_DIR/client"
LOG_DIR="$ROOT_DIR/.logs"
mkdir -p "$LOG_DIR"

info() { echo "[INFO] $*"; }
warn() { echo "[WARN] $*"; }
err()  { echo "[ERROR] $*"; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || { err "Missing command: $1"; exit 1; }; }

start_tmux_session() {
  local name="$1"
  local cmd="$2"
  if tmux has-session -t "$name" 2>/dev/null; then
    warn "tmux session '$name' already exists; restarting"
    tmux kill-session -t "$name" || true
  fi
  info "Starting $name"
  tmux new-session -d -s "$name" "bash -lc '$cmd | tee -a \"$LOG_DIR/$name.log\"'"
}

copy_env_if_missing() {
  local example="$1"
  local target="$2"
  if [[ ! -f "$target" && -f "$example" ]]; then
    cp "$example" "$target"
    info "Created $(basename "$target") from example in $(dirname "$target")"
  fi
}

upsert_env_defaults() {
  local env_file="$1"
  local json_defaults="$2"
  python3 - "$env_file" "$json_defaults" <<'PY'
from pathlib import Path
import json
import sys
p = Path(sys.argv[1])
defaults = json.loads(sys.argv[2])
text = p.read_text() if p.exists() else ""
lines = text.splitlines()
kv = {}
order = []
for line in lines:
    if '=' in line and not line.strip().startswith('#'):
        k,v = line.split('=',1)
        kv[k]=v
        if k not in order:
            order.append(k)
    else:
        order.append(line)
for k,v in defaults.items():
    if k not in kv or kv[k].startswith('your_') or not kv[k].strip():
        kv[k]=v
out=[]
seen=set()
for item in order:
    if '=' in item and not item.strip().startswith('#'):
        k,_ = item.split('=',1)
        if k in seen:
            continue
        out.append(f'{k}={kv[k]}')
        seen.add(k)
    else:
        out.append(item)
for k,v in kv.items():
    if k not in seen:
        out.append(f'{k}={v}')
        seen.add(k)
p.write_text('\n'.join(out).rstrip()+'\n')
PY
}

install_system_packages() {
  info "Installing system packages if needed"
  sudo apt-get update -y
  sudo apt-get install -y python3 python3-pip python3-venv tmux curl mongodb || true
}

install_node_if_missing() {
  if ! command -v node >/dev/null 2>&1; then
    info "Installing Node.js 22"
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
  fi
}

install_dependencies() {
  info "Installing server dependencies"
  (cd "$SERVER_DIR" && npm install)
  info "Installing client dependencies"
  (cd "$CLIENT_DIR" && npm install)
  info "Installing AI service dependencies"
  (cd "$AI_DIR" && python3 -m pip install -r requirements.txt)
}

start_mongo_if_possible() {
  if systemctl list-unit-files 2>/dev/null | grep -q '^mongod.service'; then
    info "Starting mongod via systemctl"
    sudo systemctl start mongod || true
    sudo systemctl enable mongod || true
  else
    warn "mongod system service not found; ensure MongoDB is running and MONGODB_URI is reachable"
  fi
}

show_summary() {
  echo
  echo "Services launched with tmux:"
  echo "  backend   -> http://localhost:5000"
  echo "  ai        -> http://localhost:8000"
  echo "  frontend  -> http://localhost:5173"
  echo
  echo "Useful commands:"
  echo "  tmux ls"
  echo "  tmux attach -t backend"
  echo "  tmux attach -t ai"
  echo "  tmux attach -t frontend"
  echo "  ./scripts/stop_vm.sh"
  echo
  echo "Health checks:"
  echo "  curl http://127.0.0.1:5000/"
  echo "  curl http://127.0.0.1:8000/"
  echo "  curl http://127.0.0.1:8000/agents/health"
  echo "  ss -tulnp | grep -E '5000|5173|8000'"
  echo
  echo "Logs are in: $LOG_DIR"
}

main() {
  need_cmd bash
  need_cmd curl
  need_cmd python3
  install_system_packages
  install_node_if_missing
  need_cmd npm
  need_cmd tmux

  copy_env_if_missing "$SERVER_DIR/.env.example" "$SERVER_DIR/.env"
  copy_env_if_missing "$AI_DIR/.env.example" "$AI_DIR/.env"

  upsert_env_defaults "$SERVER_DIR/.env" '{"PORT":"5000","AI_SERVICE_URL":"http://127.0.0.1:8000","BASE_URL":"http://localhost:5000"}'
  upsert_env_defaults "$AI_DIR/.env" '{"AWS_REGION":"us-west-2","BEDROCK_MODEL_ID":"anthropic.claude-3-sonnet-20240229-v1:0","FALLBACK_MODEL":"meta-llama/Meta-Llama-3.1-8B-Instruct","LLM_TIMEOUT_SECONDS":"30","LLM_CACHE_TTL_SECONDS":"300","LLM_CACHE_MAX":"128","LOG_LEVEL":"INFO"}'

  install_dependencies
  start_mongo_if_possible

  start_tmux_session backend "cd '$SERVER_DIR' && npm run dev"
  start_tmux_session ai "cd '$AI_DIR' && uvicorn app.main:app --host 0.0.0.0 --port 8000"
  start_tmux_session frontend "cd '$CLIENT_DIR' && npm run dev -- --host 0.0.0.0"

  show_summary
}

main "$@"
