export const env = {
  port: Number(process.env.PORT || 3000),
  jwtSecret: process.env.JWT_SECRET || 'dev-secret',
  orchestratorUrl: process.env.ORCHESTRATOR_URL || 'http://127.0.0.1:8001'
};
