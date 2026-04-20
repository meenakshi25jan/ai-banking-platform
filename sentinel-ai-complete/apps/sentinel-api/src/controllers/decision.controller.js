import { getDecisionById } from '../repositories/decision.repository.js';
import { getAuditEventsByDecisionId } from '../repositories/audit.repository.js';
import { buildExplanation } from '../decision/explainability.engine.js';

export async function getDecision(req, res, next) {
  try {
    const decision = await getDecisionById(req.params.id);
    if (!decision) return res.status(404).json({ error: 'Decision not found' });
    res.json(decision);
  } catch (error) {
    next(error);
  }
}

export async function explainDecision(req, res, next) {
  try {
    const decision = await getDecisionById(req.params.id);
    if (!decision) return res.status(404).json({ error: 'Decision not found' });
    res.json(buildExplanation({ decisionRecord: decision }));
  } catch (error) {
    next(error);
  }
}

export async function getDecisionAudit(req, res, next) {
  try {
    const events = await getAuditEventsByDecisionId(req.params.id);
    res.json({ decisionId: req.params.id, events });
  } catch (error) {
    next(error);
  }
}
