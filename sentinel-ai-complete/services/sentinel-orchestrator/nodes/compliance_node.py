def compliance_node(state):
    amount = float(state['input'].get('amount', 0) or 0)
    score = 0.95
    reasons = []
    if state['input'].get('crossBorder'):
        score -= 0.25
        reasons.append('Cross-border compliance review required')
    if amount >= 200000:
        score -= 0.3
        reasons.append('High-value threshold compliance check')
    state['signals']['compliance'] = {
        'name': 'compliance',
        'score': max(score, 0.0),
        'modelVersion': 'rules-compliance-v1',
        'reasons': reasons
    }
    return state
