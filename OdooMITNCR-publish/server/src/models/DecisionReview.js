const mongoose = require('mongoose');

const decisionReviewSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  governanceDecisionId: { type: mongoose.Schema.Types.ObjectId, ref: 'AiGovernanceDecision', required: true },
  status: { type: String, enum: ['pending', 'approved', 'rejected'], default: 'pending' },
  reason: { type: String },
  amount: { type: Number, required: true },
  receiverAccount: { type: String, required: true },
  description: { type: String },
  category: { type: String, default: 'Transfer' },
  resolutionNotes: { type: String },
  resolvedBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  resolvedAt: { type: Date },
}, { timestamps: true });

module.exports = mongoose.model('DecisionReview', decisionReviewSchema);
