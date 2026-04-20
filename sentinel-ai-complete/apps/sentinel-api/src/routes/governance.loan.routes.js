import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware.js';
import { validate } from '../middleware/validate.middleware.js';
import { loanSchema } from '../schemas/loan.schema.js';
import { evaluateLoanGovernance } from '../controllers/governance.loan.controller.js';

const router = Router();
router.post('/', requireAuth, validate(loanSchema), evaluateLoanGovernance);
export { router as loanGovernanceRouter };
