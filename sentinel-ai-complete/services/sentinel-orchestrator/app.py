from fastapi import FastAPI
from graphs.transfer_graph import run_transfer_graph
from graphs.login_graph import run_login_graph
from graphs.assistant_graph import run_assistant_graph
from graphs.loan_graph import run_loan_graph
from schemas import GovernanceContext

app = FastAPI(title='sentinel-orchestrator')

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'sentinel-orchestrator'}

@app.post('/orchestrate')
def orchestrate(context: GovernanceContext):
    payload = context.model_dump()
    journey = payload['journey']
    if journey == 'transfer':
        return run_transfer_graph(payload)
    if journey == 'login':
        return run_login_graph(payload)
    if journey == 'assistant':
        return run_assistant_graph(payload)
    if journey == 'loan':
        return run_loan_graph(payload)
    return {'error': f'Unsupported journey: {journey}'}
