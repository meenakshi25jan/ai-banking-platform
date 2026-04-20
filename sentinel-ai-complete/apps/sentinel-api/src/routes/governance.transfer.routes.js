import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware.js';
import { validate } from '../middleware/validate.middleware.js';
import { transferSchema } from '../schemas/transfer.schema.js';
import { evaluateTransferGovernance } from '../controllers/governance.transfer.controller.js';

const router = Router();
router.post('/', requireAuth, validate(transferSchema), evaluateTransferGovernance);
export { router as transferGovernanceRouter };
