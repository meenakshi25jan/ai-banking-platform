def behavior_node(state):
    score = 0.1
    reasons = []
    if state['input'].get('newDevice'):
        score += 0.65
        reasons.append('New device detected')
    if not state['input'].get('deviceId'):
        score += 0.08
        reasons.append('Missing device identifier')
    state['signals']['behavior'] = {
        'name': 'behavior',
        'score': min(score, 1.0),
        'modelVersion': 'hf-behavior-placeholder-v1',
        'reasons': reasons
    }
    return state
