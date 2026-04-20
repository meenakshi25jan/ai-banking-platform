from graphs.flow_builder import run_flow


def run_loan_graph(payload):
    return run_flow(payload, ['fraud', 'intent', 'behavior', 'compliance'])
