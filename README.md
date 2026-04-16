# AI-Powered Smart Banking System

A next-generation banking system combining traditional banking with AI-powered services including smart assistance, fraud detection, spending insights, predictive analysis, governed money transfers, automated loan decisions, and multi-agent AI orchestration.

## Architecture

```text
React Frontend  →  Node.js Backend  →  MongoDB
                        ↓
               Python AI Service (FastAPI)
                        ↓
  Amazon Bedrock Claude 3 Sonnet (primary)
                        ↓
  Meta-Llama-3.1-8B-Instruct / Qwen endpoint (fallback)
```

## AI optimization and governance included

- Bedrock-first LLM invocation with self-managed OpenAI-compatible fallback
- In-memory response caching for repeated prompts
- Governance scoring for fraud, behavior, intent, urgency, and compliance risk
- Structured audit logging for governance-sensitive flows
- Multi-agent orchestration via supervisor/worker pattern

## Tech Stack

- **Frontend**: React.js, Tailwind CSS, React Router, Axios, Recharts
- **Backend**: Node.js, Express.js, JWT Authentication, Mongoose
- **AI Service**: Python, FastAPI
- **Database**: MongoDB
- **Primary LLM**: Amazon Bedrock Claude 3 Sonnet
- **Fallback LLM**: Meta-Llama-3.1-8B-Instruct or Qwen via OpenAI-compatible endpoint

## Local / VM setup

### Quick start on a VM

```bash
chmod +x scripts/*.sh
FALLBACK_BASE_URL=http://<intel-server-ip>:8001 ./scripts/deploy_vm_auto.sh
```

### Manual start

#### Backend
```bash
cd server
npm install
npm run dev
```
Runs on `http://localhost:5000`

#### AI Service
```bash
cd ai-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Runs on `http://localhost:8000`

#### Frontend
```bash
cd client
npm install
npm run dev
```
Runs on `http://localhost:5173`

## Included helper scripts

- `scripts/run_vm.sh`
- `scripts/stop_vm.sh`
- `scripts/deploy_vm_auto.sh`
- `scripts/deploy_fallback_llama.sh`
- `README_VM_EXECUTION.md`

## Core features

1. **User Auth** - Register/Login with JWT
2. **Dashboard** - Account balance, recent transactions, AI predictions
3. **Transactions** - Full history with filtering
4. **Money Transfer** - Real-time AI governance and fraud controls
5. **AI Chatbot** - Bedrock-first financial assistant with fallback LLM
6. **Spending Insights** - Health score, spending breakdown, predictions
7. **Loan Eligibility** - AI-based credit scoring and loan approval
8. **Alerts** - Fraud warnings, governance review, verification requirements
