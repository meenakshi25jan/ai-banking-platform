from graphs.flow_builder import run_flow


def run_login_graph(payload):
    return run_flow(payload, ['fraud', 'behavior', 'compliance'])
