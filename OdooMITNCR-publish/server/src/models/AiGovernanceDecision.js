const mongoose = require('mongoose');

const aiGovernanceDecisionSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  transactionId: { type: mongoose.Schema.Types.ObjectId, ref: 'Transaction' },
  requestType: { type: String, default: 'transfer' },
  agentTraceId: { type: String },
  fraudScore: { type: Number, default: 0 },
  intentScore: { type: Number, default: 0 },
  behaviorScore: { type: Number, default: 0 },
  riskScore: { type: Number, default: 0 },
  complianceScore: { type: Number, default: 0 },
  finalDecision: { type: String, enum: ['allow', 'verify', 'review', 'block'], required: true },
  requiredAction: { type: String, default: 'none' },
  reason: { type: String },
  humanReviewRequired: { type: Boolean, default: false },
  payloadSummary: { type: Object },
}, { timestamps: true });

module.exports = mongoose.model('AiGovernanceDecision', aiGovernanceDecisionSchema);
