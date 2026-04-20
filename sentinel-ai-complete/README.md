# Sentinel AI Complete Scaffold

Sentinel AI is a **governed AI banking platform scaffold** for trust-centric financial workflows. This scaffold now merges the original Sentinel governance layer with the proposed AI banking direction from the companion banking project.

It includes:

- **Express API gateway** for banking and frontend integration
- **LangGraph orchestrator** for stateful governance decision flows
- **Deterministic fallback engine** so governance still works if the Python orchestrator is offline
- **PyTorch + Hugging Face model stubs** for fraud, intent, behavior, compliance, and urgency scoring
- **Deterministic policy engine** for final `ALLOW / VERIFY / BLOCK / REVIEW` outcomes
- **Audit, explainability, and review queue** persisted locally as JSON for easy demo use
- **Banking-aligned governed journeys** for login, money transfer, AI assistant, and loan intake

## What changed in this merge

This version upgrades the repo from a narrow governance demo into a stronger **governed AI banking foundation**:

- Added **urgency scoring** to reflect the banking project's governance model
- Added governed **assistant** and **loan** journeys alongside login and transfer
- Expanded transfer inputs for stronger risk evaluation
- Fixed JSON repository persistence so the API can write decision, audit, and review records correctly
- Preserved the monorepo structure so a React banking frontend and additional AI services can be attached later

## Monorepo layout

```text
apps/
  sentinel-api/
services/
  sentinel-orchestrator/
  sentinel-models/
shared/
  policies/
storage/
  decisions.json
  audits.json
  reviews.json
```

## Quick start

### 1) API
```bash
cd apps/sentinel-api
cp .env.example .env
npm install
npm run dev
```

### 2) Orchestrator
```bash
cd services/sentinel-orchestrator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8001
```

The API will call the Python orchestrator if it is available. If not, it falls back to the local deterministic engine so the demo still works.

## Main endpoints

### Core
- `GET /health`
- `GET /decision/:id`
- `GET /decision/:id/explain`
- `GET /decision/:id/audit`
- `GET /review/queue`

### Governance journeys
- `POST /governance/login`
- `POST /governance/transfer`
- `POST /governance/assistant`
- `POST /governance/loan`

### Simulation
- `POST /simulate/login`
- `POST /simulate/transfer`
- `POST /simulate/assistant`
- `POST /simulate/loan`

## Demo token

Use this JWT secret in local development: `dev-secret`

Example token payload:
```json
{ "sub": "user_1", "role": "user" }
```

Use role `reviewer` or `admin` to access the review queue.

## Suggested next steps

- Attach the **React banking frontend** from the companion project to these governance endpoints
- Replace placeholder scoring nodes with **PyTorch/Hugging Face** inference services
- Add **human-in-the-loop admin workflows** for review resolution
- Add **OpenAI or Claude-powered analyst summaries** only for explanations and reviewer assistance, not final policy decisions
- Swap local JSON persistence for MongoDB or Postgres when moving past demo mode
