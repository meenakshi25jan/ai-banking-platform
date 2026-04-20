from graphs.flow_builder import run_flow


def run_assistant_graph(payload):
    return run_flow(payload, ['intent', 'urgency', 'behavior', 'compliance'])
