import { randomUUID } from 'node:crypto';

export function requestContextMiddleware(req, _res, next) {
  req.requestContext = {
    requestId: randomUUID(),
    receivedAt: new Date().toISOString()
  };
  next();
}
