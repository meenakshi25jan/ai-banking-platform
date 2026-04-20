def intent_node(state):
    purpose = str(state['input'].get('purpose', '')).lower()
    score = 0.08
    reasons = []
    for token in ['urgent', 'immediately', 'now', 'emergency']:
        if token in purpose:
            score += 0.18
            reasons.append(f'High-pressure language detected: {token}')
    state['signals']['intent'] = {
        'name': 'intent',
        'score': min(score, 1.0),
        'modelVersion': 'hf-intent-placeholder-v1',
        'reasons': reasons
    }
    return state
