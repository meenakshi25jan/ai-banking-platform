"""Behavior profiling for banking transactions."""
from __future__ import annotations

from statistics import mean
from datetime import datetime, timedelta
from typing import Any


def _parse_dt(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def analyze_behavior(amount: float, recent_transactions: list[dict] | list[Any] | None = None) -> dict:
    recent_transactions = recent_transactions or []
    debit_amounts = []
    recent_debits = 0
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    for txn in recent_transactions:
        tx = txn.model_dump() if hasattr(txn, "model_dump") else dict(txn)
        if tx.get("type") != "debit":
            continue
        debit_amounts.append(float(tx.get("amount", 0) or 0))
        dt = _parse_dt(tx.get("createdAt"))
        if dt and dt.replace(tzinfo=None) >= five_minutes_ago:
            recent_debits += 1

    avg_debit = mean(debit_amounts) if debit_amounts else 0.0
    score = 0
    reasons: list[str] = []

    if avg_debit > 0 and amount > avg_debit * 5:
        score += 35
        reasons.append(f"Amount is {amount/avg_debit:.1f}x the recent average debit")
    elif avg_debit > 0 and amount > avg_debit * 2:
        score += 20
        reasons.append("Amount is materially above the recent debit average")

    if recent_debits >= 3:
        score += 25
        reasons.append("Rapid transfer pattern detected in the last 5 minutes")

    if not reasons:
        reasons.append("Behavior pattern looks normal")

    return {
        "behavior_risk": min(100, score),
        "is_anomalous": score >= 30,
        "avg_debit_amount": round(avg_debit, 2),
        "recent_debit_count_5m": recent_debits,
        "reason": "; ".join(reasons),
    }
