import { buildGovernanceContext } from '../context/context.builder.js';
import { orchestrateDecision } from './orchestrator.client.js';
import { createDecisionRecord, getDecisionById } from '../repositories/decision.repository.js';
import { recordAudit } from '../audit/audit.service.js';
import { createReviewCase } from '../review/review.service.js';

function nextStepFor(journey, decision) {
  if (decision === 'ALLOW') {
    if (journey === 'assistant') return 'RESPOND_TO_USER';
    if (journey === 'loan') return 'PROCEED_TO_ELIGIBILITY_OR_UNDERWRITING';
    return 'EXECUTE_TRANSACTION';
  }
  if (decision === 'VERIFY') {
    if (journey === 'loan') return 'REQUEST_BORROWER_VERIFICATION_DOCUMENTS';
    if (journey === 'assistant') return 'STEP_UP_IDENTITY_OR_CONTEXT_VERIFICATION';
    return 'OTP_OR_VOICE_VERIFICATION';
  }
  if (decision === 'BLOCK') return 'STOP_AND_NOTIFY';
  return 'SEND_TO_MANUAL_REVIEW';
}

export async function executeJourney({ journey, input, auth, requestContext }) {
  const context = buildGovernanceContext({ journey, input, auth, requestContext });
  const result = await orchestrateDecision(context);
  const decisionRecord = await createDecisionRecord({ ...result.decision, input: context.input, signals: result.signals });
  await recordAudit({
    decisionId: decisionRecord.id,
    eventType: 'DECISION_CREATED',
    actor: 'sentinel-ai',
    payload: result,
  });
  if (result.decision.decision === 'REVIEW') {
    await createReviewCase({
      decisionId: decisionRecord.id,
      summary: result.decision.reasons.join('; '),
      priority: result.decision.trustScore < 40 ? 'HIGH' : 'MEDIUM',
    });
  }
  const saved = await getDecisionById(decisionRecord.id);
  return {
    decisionId: saved.id,
    journey,
    decision: saved.decision,
    trustScore: saved.trustScore,
    reasons: saved.reasons,
    nextStep: nextStepFor(journey, saved.decision),
  };
}

export async function simulateJourney({ journey, input, auth, requestContext }) {
  const context = buildGovernanceContext({ journey, input, auth, requestContext });
  return orchestrateDecision(context);
}
