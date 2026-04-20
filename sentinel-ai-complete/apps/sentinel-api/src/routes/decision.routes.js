import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware.js';
import { getDecision, explainDecision, getDecisionAudit } from '../controllers/decision.controller.js';

const router = Router();
router.get('/:id', requireAuth, getDecision);
router.get('/:id/explain', requireAuth, explainDecision);
router.get('/:id/audit', requireAuth, getDecisionAudit);
export { router as decisionRouter };
