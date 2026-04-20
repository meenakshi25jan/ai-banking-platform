import { createAuditEvent } from '../repositories/audit.repository.js';

export async function recordAudit({ decisionId, eventType, actor, payload }) {
  return createAuditEvent({ decisionId, eventType, actor, payload });
}
