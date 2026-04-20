from graphs.flow_builder import run_flow


def run_transfer_graph(payload):
    return run_flow(payload, ['fraud', 'intent', 'urgency', 'behavior', 'compliance'])
