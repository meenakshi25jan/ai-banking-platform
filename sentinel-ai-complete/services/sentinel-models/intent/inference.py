"""Intent model placeholder."""

def predict(features: dict) -> dict:
    purpose = str(features.get('purpose', '')).lower()
    score = 0.08 + (0.2 if 'urgent' in purpose else 0)
    return {
        'score': min(score, 1.0),
        'confidence': 0.79,
        'modelVersion': 'intent-placeholder-v1',
        'reasons': ['Replace with trained PyTorch/HF model']
    }
