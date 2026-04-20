import { executeJourney } from '../services/governance.service.js';

export async function evaluateTransferGovernance(req, res, next) {
  try {
    const result = await executeJourney({
      journey: 'transfer',
      input: req.validatedBody,
      auth: req.auth,
      requestContext: req.requestContext
    });
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
}
