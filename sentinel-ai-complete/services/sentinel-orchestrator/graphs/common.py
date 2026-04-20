from pathlib import Path
import json
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_DIR = REPO_ROOT / 'shared' / 'policies'


def get_value(data, dotted):
    current = data
    for part in dotted.split('.'):
        current = current.get(part)
        if current is None:
            return None
    return current


def compare(left, operator, right):
    if operator == '>':
        return left > right
    if operator == '>=':
        return left >= right
    if operator == '<':
        return left < right
    if operator == '<=':
        return left <= right
    if operator == '===':
        return left == right
    return False


def load_policy(journey: str):
    return json.loads((POLICY_DIR / f'{journey}.v1.json').read_text())


def calculate_trust_score(signals):
    fraud = signals.get('fraud', {}).get('score', 0)
    intent = signals.get('intent', {}).get('score', 0)
    behavior = signals.get('behavior', {}).get('score', 0)
    compliance = signals.get('compliance', {}).get('score', 1)
    trust = (1 - fraud) * 35 + (1 - intent) * 20 + (1 - behavior) * 20 + compliance * 25
    return max(0, min(100, round(trust)))


def evaluate_policy(policy, signals):
    rules = sorted(policy['rules'], key=lambda item: item['priority'], reverse=True)
    for rule in rules:
        left = get_value(signals, rule['field'])
        if compare(left, rule['operator'], rule['value']):
            return {
                'decision': rule['decision'],
                'reason': rule['reason'],
                'ruleId': rule['id'],
                'policyVersion': policy['version']
            }
    return {
        'decision': 'ALLOW',
        'reason': 'No blocking or review policy triggered',
        'ruleId': 'default-allow',
        'policyVersion': policy['version']
    }


def finalize_response(state):
    policy = load_policy(state['journey'])
    policy_result = evaluate_policy(policy, state['signals'])
    reasons = [policy_result['reason']]
    for signal in state['signals'].values():
        reasons.extend(signal.get('reasons', []))
    return {
        'traceId': str(uuid4()),
        'signals': state['signals'],
        'policyResult': policy_result,
        'decision': {
            'journey': state['journey'],
            'actor': state['actor'],
            'decision': policy_result['decision'],
            'trustScore': calculate_trust_score(state['signals']),
            'reasons': list(dict.fromkeys(reasons)),
            'policyVersion': policy_result['policyVersion'],
            'ruleId': policy_result['ruleId'],
            'createdAt': state.get('receivedAt')
        }
    }
