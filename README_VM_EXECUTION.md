# VM Execution Guide

This repository includes scripts to deploy and run the platform on a Linux VM and to start a self-managed Llama fallback server on a separate Intel/Linux host.

## Included scripts

- `scripts/run_vm.sh` — installs dependencies and starts backend, AI service, and frontend in tmux
- `scripts/stop_vm.sh` — stops those tmux sessions
- `scripts/deploy_vm_auto.sh` — patches `.env` files from exported variables, then runs the stack
- `scripts/deploy_fallback_llama.sh` — installs `llama.cpp`, downloads Meta-Llama-3.1-8B-Instruct GGUF, and starts the fallback server on port `8001`

## Services and ports

- Backend: `http://localhost:5000`
- AI service: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Fallback LLM server: `http://<intel-host>:8001`

## Fastest path on the VM

From the project root:

```bash
chmod +x scripts/*.sh
FALLBACK_BASE_URL=http://<intel-server-ip>:8001 ./scripts/deploy_vm_auto.sh
```

If Bedrock credentials are available on the VM, include them too:

```bash
AWS_ACCESS_KEY_ID=... \
AWS_SECRET_ACCESS_KEY=... \
AWS_REGION=us-west-2 \
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0 \
FALLBACK_BASE_URL=http://<intel-server-ip>:8001 \
./scripts/deploy_vm_auto.sh
```

## Fallback Llama deployment on the Intel server

Run on the Intel/Linux server:

```bash
chmod +x scripts/deploy_fallback_llama.sh
./scripts/deploy_fallback_llama.sh
```

That script starts `llama-server` inside tmux on port `8001` using `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`.

## Environment files

### `server/.env`

```env
PORT=5000
MONGODB_URI=mongodb://127.0.0.1:27017/aibanking
JWT_SECRET=change_me
AI_SERVICE_URL=http://127.0.0.1:8000
BASE_URL=http://localhost:5000
```

### `ai-service/.env`

```env
AWS_REGION=us-west-2
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
FALLBACK_BASE_URL=http://<intel-server-ip>:8001
FALLBACK_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct
LLM_TIMEOUT_SECONDS=30
LLM_CACHE_TTL_SECONDS=300
LLM_CACHE_MAX=128
AUDIT_LOG_PATH=audit.log
LOG_LEVEL=INFO
```

## Verification

```bash
tmux ls
curl http://127.0.0.1:5000/
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/agents/health
ss -tulnp | grep -E '5000|5173|8000'
```

## Notes

- The AI service prefers Bedrock Claude 3 Sonnet and falls back to a self-managed OpenAI-compatible endpoint such as Meta-Llama or Qwen.
- Governance decisions are audit-logged to `audit.log` by default.
- For production deployment, use Docker/ECS instead of the VM helper scripts.
