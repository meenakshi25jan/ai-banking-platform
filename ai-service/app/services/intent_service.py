"""Intent analysis for banking transfer requests."""
from __future__ import annotations

from typing import Iterable

URGENCY_PATTERNS = {
    "urgent", "immediately", "immediate", "asap", "right now", "emergency",
    "quickly", "fast", "hurry", "don't tell", "dont tell", "secret", "confidential",
}

SOCIAL_ENGINEERING_PATTERNS = {
    "otp", "bank support", "customer care", "remote access", "screen share",
    "verify account", "kyc update", "gift card", "refund", "refund link",
}


def analyze_intent(description: str | None = None, message: str | None = None) -> dict:
    text = f"{description or ''} {message or ''}".strip().lower()
    matches: list[str] = []

    for pattern in sorted(URGENCY_PATTERNS | SOCIAL_ENGINEERING_PATTERNS):
        if pattern in text:
            matches.append(pattern)

    urgency_hits = sum(1 for p in matches if p in URGENCY_PATTERNS)
    social_hits = sum(1 for p in matches if p in SOCIAL_ENGINEERING_PATTERNS)

    score = min(100, urgency_hits * 20 + social_hits * 25)
    suspicious = score >= 30

    if not text:
        reason = "No free-text intent signals provided"
    elif suspicious:
        reason = f"Suspicious intent cues detected: {', '.join(matches[:5])}"
    else:
        reason = "No suspicious intent cues detected"

    return {
        "intent_risk": score,
        "suspicious": suspicious,
        "matched_signals": matches,
        "reason": reason,
    }
