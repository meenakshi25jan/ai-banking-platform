import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware.js';
import { validate } from '../middleware/validate.middleware.js';
import { assistantSchema } from '../schemas/assistant.schema.js';
import { evaluateAssistantGovernance } from '../controllers/governance.assistant.controller.js';

const router = Router();
router.post('/', requireAuth, validate(assistantSchema), evaluateAssistantGovernance);
export { router as assistantGovernanceRouter };
