def urgency_node(state):
    score = 0.05
    reasons = []
    purpose = str(state['input'].get('purpose', '')).lower()
    note = str(state['input'].get('message', '')).lower()
    combined = f'{purpose} {note}'
    for token in ['urgent', 'immediately', 'now', 'emergency', 'asap']:
        if token in combined:
            score += 0.18
            reasons.append(f'Urgency language detected: {token}')
    if state['input'].get('expediteRequested'):
        score += 0.2
        reasons.append('Customer requested expedited handling')
    state['signals']['urgency'] = {
        'name': 'urgency',
        'score': min(score, 1.0),
        'modelVersion': 'hf-urgency-placeholder-v1',
        'reasons': reasons
    }
    return state
