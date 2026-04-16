# Agentic AI Governance Implementation

## What was added

This upgrade adds a dedicated governance boundary between AI reasoning and banking execution.

### New AI services
- `intent_service.py` — flags urgency, coercion, suspicious language, and manipulation cues.
- `behavior_service.py` — detects anomalous transfer behavior relative to recent history.
- `governance_service.py` — combines fraud, intent, and behavior into a governed decision.

### New governed endpoint
- `POST /agents/governed-transfer-risk`

### New backend models
- `AiGovernanceDecision` — stores final governed decision, scores, trace ID, reason, and action.
- `DecisionReview` — stores manual review items for high-risk or ambiguous actions.

### New backend policy mapping
- `policyEngine.js` maps AI governance decisions into runtime actions:
  - `allow`
  - `verify`
  - `review`
  - `block`

## Runtime flow
1. User initiates transfer.
2. Backend calls `/agents/governed-transfer-risk`.
3. AI layer runs fraud, intent, and behavior analysis.
4. Governance service returns governed decision and reason.
5. Backend stores governance audit record.
6. Backend enforces action:
   - allow: execute transfer
   - verify: require OTP/voice/post-transfer verification
   - review: create manual review item
   - block: block transaction and create alert

## Current status
- Governance decisioning is implemented.
- Audit and review records are implemented.
- Admin review routes are implemented.
- Verify path is returned as a policy action and can be connected to OTP/IVR/UI workflows.

## Suggested next work
- Add frontend screens for pending reviews and verification prompts.
- Wire verification types directly into OTP / Exotel / AWS Connect.
- Add richer compliance rules (beneficiary novelty, device trust, IP drift).
- Add analytics dashboards for governed outcomes.
