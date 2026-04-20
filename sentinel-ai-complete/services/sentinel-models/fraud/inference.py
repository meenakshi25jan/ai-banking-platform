"""Fraud model placeholder.
Swap this file with a real PyTorch/Hugging Face inference endpoint or batch service.
"""

def predict(features: dict) -> dict:
    amount = float(features.get('amount', 0) or 0)
    score = min(0.1 + (0.5 if amount >= 100000 else 0), 1.0)
    return {
        'score': score,
        'confidence': 0.8,
        'modelVersion': 'fraud-placeholder-v1',
        'reasons': ['Replace with trained PyTorch/HF model']
    }
