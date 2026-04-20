export function buildExplanation({ decisionRecord }) {
  return {
    decisionId: decisionRecord.id,
    journey: decisionRecord.journey,
    actor: decisionRecord.actor,
    decision: decisionRecord.decision,
    trustScore: decisionRecord.trustScore,
    reasons: decisionRecord.reasons,
    signals: decisionRecord.signals,
    policyVersion: decisionRecord.policyVersion,
    ruleId: decisionRecord.ruleId,
    createdAt: decisionRecord.createdAt
  };
}
