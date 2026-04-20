export function buildGovernanceContext({ journey, input, auth, requestContext }) {
  return {
    journey,
    actor: {
      userId: auth?.sub || input.userId,
      role: auth?.role || 'user'
    },
    input,
    requestContext,
    metadata: {
      receivedAt: new Date().toISOString()
    }
  };
}
