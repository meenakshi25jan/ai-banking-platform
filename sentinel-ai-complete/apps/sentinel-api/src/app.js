import express from 'express';
import { requestContextMiddleware } from './middleware/requestContext.middleware.js';
import { errorHandler } from './middleware/error.middleware.js';
import { healthRouter } from './routes/health.routes.js';
import { loginGovernanceRouter } from './routes/governance.login.routes.js';
import { transferGovernanceRouter } from './routes/governance.transfer.routes.js';
import { assistantGovernanceRouter } from './routes/governance.assistant.routes.js';
import { loanGovernanceRouter } from './routes/governance.loan.routes.js';
import { decisionRouter } from './routes/decision.routes.js';
import { reviewRouter } from './routes/review.routes.js';
import { simulationRouter } from './routes/simulation.routes.js';

const app = express();
app.use(express.json());
app.use(requestContextMiddleware);
app.use('/health', healthRouter);
app.use('/governance/login', loginGovernanceRouter);
app.use('/governance/transfer', transferGovernanceRouter);
app.use('/governance/assistant', assistantGovernanceRouter);
app.use('/governance/loan', loanGovernanceRouter);
app.use('/decision', decisionRouter);
app.use('/review', reviewRouter);
app.use('/simulate', simulationRouter);
app.use(errorHandler);

export { app };
