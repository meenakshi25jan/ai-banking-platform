#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<USAGE
Usage:
  FALLBACK_BASE_URL=http://<intel-server>:8001 ./scripts/deploy_vm_auto.sh

Optional env vars:
  MONGODB_URI=...                     MongoDB connection string
  AWS_ACCESS_KEY_ID=...               Bedrock access key
  AWS_SECRET_ACCESS_KEY=...           Bedrock secret
  AWS_REGION=us-west-2                AWS region
  BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
  FALLBACK_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

cp -n "$ROOT_DIR/server/.env.example" "$ROOT_DIR/server/.env" || true
cp -n "$ROOT_DIR/ai-service/.env.example" "$ROOT_DIR/ai-service/.env" || true

python3 - "$ROOT_DIR" <<'PY'
from pathlib import Path
import os, sys
root = Path(sys.argv[1])

def patch(path, updates):
    p = Path(path)
    lines = p.read_text().splitlines() if p.exists() else []
    kv = {}
    for line in lines:
        if '=' in line and not line.strip().startswith('#'):
            k,v = line.split('=',1)
            kv[k]=v
    kv.update({k:v for k,v in updates.items() if v is not None and v != ''})
    ordered = []
    seen = set()
    for line in lines:
        if '=' in line and not line.strip().startswith('#'):
            k,_ = line.split('=',1)
            if k in seen: continue
            ordered.append(f"{k}={kv.get(k,'')}")
            seen.add(k)
        else:
            ordered.append(line)
    for k,v in kv.items():
        if k not in seen:
            ordered.append(f"{k}={v}")
    p.write_text("\n".join(ordered).rstrip()+"\n")

patch(root/'server/.env', {
    'MONGODB_URI': os.getenv('MONGODB_URI', ''),
    'AI_SERVICE_URL': 'http://127.0.0.1:8000',
})
patch(root/'ai-service/.env', {
    'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID', ''),
    'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
    'AWS_REGION': os.getenv('AWS_REGION', 'us-west-2'),
    'BEDROCK_MODEL_ID': os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0'),
    'FALLBACK_BASE_URL': os.getenv('FALLBACK_BASE_URL', ''),
    'FALLBACK_MODEL': os.getenv('FALLBACK_MODEL', 'meta-llama/Meta-Llama-3.1-8B-Instruct'),
})
PY

exec "$ROOT_DIR/scripts/run_vm.sh"
