import { Router } from 'express';
import { requireAuth } from '../middleware/auth.middleware.js';
import { validate } from '../middleware/validate.middleware.js';
import { transferSchema } from '../schemas/transfer.schema.js';
import { loginSchema } from '../schemas/login.schema.js';
import { assistantSchema } from '../schemas/assistant.schema.js';
import { loanSchema } from '../schemas/loan.schema.js';
import { simulateJourney } from '../services/governance.service.js';

const router = Router();

function simulationHandler(journey, schema) {
  return [
    requireAuth,
    validate(schema),
    async (req, res, next) => {
      try {
        const result = await simulateJourney({ journey, input: req.validatedBody, auth: req.auth, requestContext: req.requestContext });
        res.json({ mode: 'simulation', ...result });
      } catch (error) {
        next(error);
      }
    }
  ];
}

router.post('/transfer', ...simulationHandler('transfer', transferSchema));
router.post('/login', ...simulationHandler('login', loginSchema));
router.post('/assistant', ...simulationHandler('assistant', assistantSchema));
router.post('/loan', ...simulationHandler('loan', loanSchema));

export { router as simulationRouter };
