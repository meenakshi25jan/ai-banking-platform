import { executeJourney } from '../services/governance.service.js';

export async function evaluateAssistantGovernance(req, res, next) {
  try {
    const result = await executeJourney({
      journey: 'assistant',
      input: req.validatedBody,
      auth: req.auth,
      requestContext: req.requestContext,
    });
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
}
