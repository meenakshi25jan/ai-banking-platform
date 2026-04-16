"""Decision-to-action governance for agentic banking workflows."""
from __future__ import annotations

import re

_HIGH_RISK_PATTERNS = (
    (r"\b(urgent|immediately|right now|asap)\b", "Urgency language detected", 18),
    (r"\b(otp|one[ -]?time password|pin|cvv|password)\b", "Sensitive credential language detected", 30),
    (r"\b(gift card|crypto|bitcoin|usdt|wallet)\b", "High-risk payment rail detected", 20),
    (r"\b(new account|new beneficiary|unknown receiver)\b", "New beneficiary language detected", 15),
    (r"\b(family emergency|legal issue|police|customs|refund scam)\b", "Possible social engineering pattern detected", 22),
)


def _keyword_risk(text: str | None):
    if not text:
        return 0, []
    total = 0
    reasons = []
    for pattern, reason, score in _HIGH_RISK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            total += score
            reasons.append(reason)
    return min(100, total), reasons


def evaluate_governance(
    amount: float,
    fraud_result: dict | None = None,
    intent_result: dict | None = None,
    behavior_result: dict | None = None,
    description: str | None = None,
    message: str | None = None,
) -> dict:
    fraud_result = fraud_result or {}
    intent_result = intent_result or {}
    behavior_result = behavior_result or {}

    fraud_score = float(fraud_result.get("risk_score", 0) or 0)
    intent_score = float(intent_result.get("intent_risk", 0) or 0)
    behavior_score = float(behavior_result.get("behavior_risk", 0) or 0)

    keyword_score, keyword_reasons = _keyword_risk(" ".join(filter(None, [description or "", message or ""])))

    amount_risk = 0
    if amount >= 500000:
        amount_risk = 30
    elif amount >= 100000:
        amount_risk = 18
    elif amount >= 50000:
        amount_risk = 10

    weighted_risk = min(100, round(fraud_score * 0.4 + intent_score * 0.2 + behavior_score * 0.2 + keyword_score * 0.2 + amount_risk, 2))
    compliance_score = min(100, round(weighted_risk * 0.75 + amount_risk, 2))

    if weighted_risk >= 85 or compliance_score >= 85:
        decision = "block"
        required_action = "none"
        human_review = True
    elif weighted_risk >= 65 or compliance_score >= 70:
        decision = "review"
        required_action = "human_review"
        human_review = True
    elif amount >= 100000:
        decision = "verify"
        required_action = "post_transfer_verification"
        human_review = False
    elif weighted_risk >= 45:
        decision = "verify"
        required_action = "voice_verification"
        human_review = False
    elif weighted_risk >= 25:
        decision = "verify"
        required_action = "otp"
        human_review = False
    else:
        decision = "allow"
        required_action = "none"
        human_review = False

    reasons = [
        fraud_result.get("reason"),
        intent_result.get("reason"),
        behavior_result.get("reason"),
        *keyword_reasons,
    ]
    reasons = [r for r in reasons if r]

    return {
        "decision": decision,
        "risk_score": weighted_risk,
        "compliance_score": compliance_score,
        "required_action": required_action,
        "requires_human_review": human_review,
        "fraud_score": fraud_score,
        "intent_score": intent_score,
        "behavior_score": behavior_score,
        "keyword_risk": keyword_score,
        "amount_risk": amount_risk,
        "reason": " | ".join(reasons) if reasons else "No governance issues detected",
    }
