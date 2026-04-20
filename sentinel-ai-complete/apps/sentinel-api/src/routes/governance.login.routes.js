import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware.js';
import { validate } from '../middleware/validate.middleware.js';
import { loginSchema } from '../schemas/login.schema.js';
import { evaluateLoginGovernance } from '../controllers/governance.login.controller.js';

const router = Router();
router.post('/', requireAuth, validate(loginSchema), evaluateLoginGovernance);
export { router as loginGovernanceRouter };
