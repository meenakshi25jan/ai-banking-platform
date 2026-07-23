function mapGovernanceDecision(governance = {}) {
  const decision = governance.decision || 'allow';
  switch (decision) {
    case 'block':
      return { action: 'block', verificationRequired: false };
    case 'review':
      return { action: 'review', verificationRequired: false };
    case 'verify':
      return {
        action: 'verify',
        verificationRequired: true,
        verificationType: governance.required_action || 'otp',
      };
    default:
      return { action: 'allow', verificationRequired: false };
  }
}

module.exports = { mapGovernanceDecision };
