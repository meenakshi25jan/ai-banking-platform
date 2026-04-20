from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, END
from graphs.common import finalize_response
from nodes.fraud_node import fraud_node
from nodes.intent_node import intent_node
from nodes.behavior_node import behavior_node
from nodes.compliance_node import compliance_node
from nodes.urgency_node import urgency_node

NODE_MAP = {
    'fraud': fraud_node,
    'intent': intent_node,
    'behavior': behavior_node,
    'compliance': compliance_node,
    'urgency': urgency_node,
}

class JourneyState(TypedDict):
    journey: str
    actor: Dict[str, Any]
    input: Dict[str, Any]
    receivedAt: str
    signals: Dict[str, Any]


def start_state(payload):
    return {
        'journey': payload['journey'],
        'actor': payload['actor'],
        'input': payload['input'],
        'receivedAt': payload.get('metadata', {}).get('receivedAt'),
        'signals': {}
    }


def run_flow(payload, ordered_nodes: List[str]):
    graph = StateGraph(JourneyState)
    for name in ordered_nodes:
        graph.add_node(name, NODE_MAP[name])
    graph.set_entry_point(ordered_nodes[0])
    for current, next_name in zip(ordered_nodes, ordered_nodes[1:]):
        graph.add_edge(current, next_name)
    graph.add_edge(ordered_nodes[-1], END)
    compiled = graph.compile()
    state = compiled.invoke(start_state(payload))
    return finalize_response(state)
