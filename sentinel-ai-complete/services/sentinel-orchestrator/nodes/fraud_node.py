def fraud_node(state):
    amount = float(state['input'].get('amount', 0) or 0)
    cross_border = bool(state['input'].get('crossBorder'))
    failed_attempts = int(state['input'].get('failedAttemptsLast24h', 0) or 0)
    score = 0.12
    reasons = []
    if amount >= 100000:
        score += 0.5
        reasons.append('High-value transfer')
    if amount >= 25000:
        score += 0.12
        reasons.append('Elevated transfer amount')
    if cross_border:
        score += 0.2
        reasons.append('Cross-border activity')
    if failed_attempts >= 5:
        score += 0.25
        reasons.append('Repeated failed attempts')
    state['signals']['fraud'] = {
        'name': 'fraud',
        'score': min(score, 1.0),
        'modelVersion': 'hf-fraud-placeholder-v1',
        'reasons': reasons
    }
    return state
