const Transaction = require('../models/Transaction');
const Account = require('../models/Account');
const Alert = require('../models/Alert');
const User = require('../models/User');
const PendingTransfer = require('../models/PendingTransfer');
const PostTransferVerification = require('../models/PostTransferVerification');
const AiGovernanceDecision = require('../models/AiGovernanceDecision');
const DecisionReview = require('../models/DecisionReview');
const axios = require('axios');
const { makeVerificationCall, getCallStatus, assessTransferRisk } = require('../services/exotelService');
const { makeVerificationCall: makeConnectCall } = require('../services/awsConnectService');
const { mapGovernanceDecision } = require('../services/policyEngine');

exports.getTransactions = async (req, res) => {
  try {
    const transactions = await Transaction.find({ userId: req.userId })
      .sort({ createdAt: -1 })
      .limit(50);
    res.json(transactions);
  } catch (error) {
    res.status(500).json({ message: 'Server error.', error: error.message });
  }
};

exports.transfer = async (req, res) => {
  try {
    const { receiverAccount, amount, category, description } = req.body;

    if (!receiverAccount || !amount || amount <= 0) {
      return res.status(400).json({ message: 'Invalid transfer details.' });
    }

    const senderAcc = await Account.findOne({ userId: req.userId });
    if (!senderAcc) return res.status(404).json({ message: 'Sender account not found.' });

    if (senderAcc.isHeld) {
      return res.status(403).json({
        message: 'Your account is temporarily held for security review. Please contact admin.',
        held: true,
        heldReason: senderAcc.heldReason,
      });
    }

    if (senderAcc.balance < amount) {
      return res.status(400).json({ message: 'Insufficient balance.' });
    }

    const receiverAcc = await Account.findOne({ accountNumber: receiverAccount });
    if (!receiverAcc) return res.status(404).json({ message: 'Receiver account not found.' });

    if (senderAcc.accountNumber === receiverAccount) {
      return res.status(400).json({ message: 'Cannot transfer to your own account.' });
    }

    const senderUser = await User.findById(req.userId);
    const receiverUser = await User.findById(receiverAcc.userId);

    const recentTxns = await Transaction.find({ userId: req.userId })
      .sort({ createdAt: -1 }).limit(10);

    let governed = {
      decision: 'allow',
      risk_score: 0,
      compliance_score: 0,
      required_action: 'none',
      requires_human_review: false,
      fraud_score: 0,
      intent_score: 0,
      behavior_score: 0,
      reason: 'AI governance service unavailable, default allow path used.',
      trace: null,
    };

    try {
      const response = await axios.post(`${process.env.AI_SERVICE_URL}/agents/governed-transfer-risk`, {
        amount,
        balance: senderAcc.balance,
        description,
        message: description,
        recent_transactions: recentTxns.map(t => ({ amount: t.amount, type: t.type, createdAt: t.createdAt })),
      }, { timeout: 5000 });

      const result = response.data?.result || {};
      governed = {
        decision: result.decision || 'allow',
        risk_score: result.risk_score || 0,
        compliance_score: result.compliance_score || 0,
        required_action: result.required_action || 'none',
        requires_human_review: !!result.requires_human_review,
        fraud_score: result.fraud_score || 0,
        intent_score: result.intent_score || 0,
        behavior_score: result.behavior_score || 0,
        reason: result.reason || 'Governance decision completed',
        trace: response.data?.trace || null,
      };
    } catch (err) {
      console.warn('[Governance] AI service unavailable:', err.message);
    }

    const governanceRecord = await AiGovernanceDecision.create({
      userId: req.userId,
      requestType: 'transfer',
      agentTraceId: governed.trace?.trace_id,
      fraudScore: governed.fraud_score,
      intentScore: governed.intent_score,
      behaviorScore: governed.behavior_score,
      riskScore: governed.risk_score,
      complianceScore: governed.compliance_score,
      finalDecision: governed.decision,
      requiredAction: governed.required_action,
      reason: governed.reason,
      humanReviewRequired: governed.requires_human_review,
      payloadSummary: { receiverAccount, amount, category, description },
    });

    const policy = mapGovernanceDecision(governed);

    if (policy.action === 'block') {
      await Alert.create({
        userId: req.userId,
        type: 'fraud',
        message: governed.reason || 'Suspicious transaction detected and blocked.',
        severity: 'high',
      });

      await Transaction.create({
        userId: req.userId,
        type: 'debit',
        amount,
        category: category || 'Transfer',
        receiver: receiverAccount,
        description,
        status: 'blocked',
      });

      return res.status(403).json({
        message: 'Transaction blocked by governance policy.',
        fraud: true,
        decision: governed.decision,
        reason: governed.reason,
        governanceDecisionId: governanceRecord._id,
      });
    }

    if (policy.action === 'review') {
      const pendingTxn = await Transaction.create({
        userId: req.userId,
        type: 'debit',
        amount,
        category: category || 'Transfer',
        receiver: receiverUser ? receiverUser.name : receiverAccount,
        description: `[PENDING REVIEW] ${description || ''}`,
        status: 'pending',
      });

      governanceRecord.transactionId = pendingTxn._id;
      await governanceRecord.save();

      const review = await DecisionReview.create({
        userId: req.userId,
        governanceDecisionId: governanceRecord._id,
        reason: governed.reason,
        amount,
        receiverAccount,
        description,
        category: category || 'Transfer',
      });

      await Alert.create({
        userId: req.userId,
        type: 'warning',
        message: 'Your transfer has been held for manual review.',
        severity: 'medium',
      });

      return res.status(202).json({
        message: 'Transfer held for manual review.',
        decision: governed.decision,
        reason: governed.reason,
        governanceDecisionId: governanceRecord._id,
        reviewId: review._id,
      });
    }

    if (policy.action === 'verify') {
      const pendingTxn = await Transaction.create({
        userId: req.userId,
        type: 'debit',
        amount,
        category: category || 'Transfer',
        receiver: receiverUser ? receiverUser.name : receiverAccount,
        description: `[PENDING ${policy.verificationType?.toUpperCase()}] ${description || ''}`,
        status: 'pending',
      });

      governanceRecord.transactionId = pendingTxn._id;
      await governanceRecord.save();

      return res.status(202).json({
        message: 'Additional verification required before transfer execution.',
        decision: governed.decision,
        requiredAction: policy.verificationType,
        governanceDecisionId: governanceRecord._id,
        pendingTransactionId: pendingTxn._id,
        reason: governed.reason,
      });
    }

    senderAcc.balance -= amount;
    receiverAcc.balance += amount;
    await senderAcc.save();
    await receiverAcc.save();

    const txn = await Transaction.create({
      userId: req.userId,
      type: 'debit',
      amount,
      category: category || 'Transfer',
      receiver: receiverUser ? receiverUser.name : receiverAccount,
      description,
      status: 'success',
    });

    governanceRecord.transactionId = txn._id;
    await governanceRecord.save();

    await Transaction.create({
      userId: receiverAcc.userId,
      type: 'credit',
      amount,
      category: category || 'Transfer',
      sender: senderUser ? senderUser.name : 'Unknown',
      description: `Transfer from ${senderUser ? senderUser.name : 'Unknown'}`,
      status: 'success',
    });

    let verificationId = null;
    if (amount >= 100000) {
      try {
        const senderPhone = senderUser?.phone || req.body.phoneNumber || '+917020542266';
        const verification = await PostTransferVerification.create({
          userId: req.userId,
          transactionId: txn._id,
          receiverAccount,
          amount,
          beneficiaryName: receiverUser?.name || receiverAccount,
          phoneNumber: senderPhone,
          status: 'pending',
        });

        makeConnectCall(senderPhone, verification._id.toString(), {
          amount,
          receiverAccount,
          beneficiaryName: receiverUser?.name || '',
        }).then(async (callResult) => {
          if (callResult.success) {
            verification.status = 'calling';
            verification.contactId = callResult.contactId;
            await verification.save();
          }
        }).catch(err => console.error('[Post-Transfer Verify] Call error:', err.message));

        verificationId = verification._id;
      } catch (verifyErr) {
        console.error('[Post-Transfer Verify] Error:', verifyErr.message);
      }
    }

    res.json({
      message: 'Transfer successful.',
      transaction: txn,
      newBalance: senderAcc.balance,
      governanceDecisionId: governanceRecord._id,
      verificationId,
      verificationRequired: amount >= 100000,
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error.', error: error.message });
  }
};

/**
 * Initiate a voice-verified transfer.
 * Runs risk assessment → creates pending transfer → triggers Exotel call.
 */
exports.transferWithVoice = async (req, res) => {
  try {
    const { receiverAccount, amount, category, description, beneficiaryName, ifsc, phoneNumber } = req.body;

    if (!receiverAccount || !amount || amount <= 0) {
      return res.status(400).json({ message: 'Invalid transfer details.' });
    }
    if (!phoneNumber) {
      return res.status(400).json({ message: 'Phone number required for voice verification.' });
    }

    const senderAcc = await Account.findOne({ userId: req.userId });
    if (!senderAcc) return res.status(404).json({ message: 'Sender account not found.' });

    // Block transfers from held accounts
    if (senderAcc.isHeld) {
      return res.status(403).json({
        message: 'Your account is temporarily held for security review. Please contact admin.',
        held: true,
        heldReason: senderAcc.heldReason,
      });
    }

    if (senderAcc.balance < amount) {
      return res.status(400).json({ message: 'Insufficient balance.' });
    }

    // Risk assessment
    const recentTxns = await Transaction.find({ userId: req.userId })
      .sort({ createdAt: -1 }).limit(20);
    const risk = assessTransferRisk(amount, senderAcc.balance, recentTxns);

    // Create pending transfer
    const pending = await PendingTransfer.create({
      userId: req.userId,
      receiverAccount,
      amount: Number(amount),
      category: category || 'Transfer',
      description: description || '',
      beneficiaryName: beneficiaryName || '',
      ifsc: ifsc || '',
      phoneNumber,
      status: 'pending',
      riskLevel: risk.level,
      riskReason: risk.reason,
    });

    // Trigger Exotel voice call
    const callResult = await makeVerificationCall(phoneNumber, pending._id.toString());

    if (callResult.success) {
      pending.status = 'calling';
      if (callResult.callSid) pending.callSid = callResult.callSid;
      await pending.save();
    }
    // Even if call fails, the pending transfer stays for simulation/manual flow

    res.json({
      message: 'Voice verification initiated.',
      pendingTransferId: pending._id,
      status: pending.status,
      riskLevel: risk.level,
      riskReason: risk.reason,
      callInitiated: callResult.success,
      callReason: callResult.reason || null,
      phoneNumber: phoneNumber.replace(/.(?=.{4})/g, '*'), // Mask number
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error.', error: error.message });
  }
};

/**
 * Check status of a pending voice-verified transfer.
 * Also polls Exotel call status when a callSid exists.
 */
exports.getPendingTransferStatus = async (req, res) => {
  try {
    const { id } = req.params;
    const pending = await PendingTransfer.findOne({ _id: id, userId: req.userId });

    if (!pending) {
      return res.status(404).json({ message: 'Pending transfer not found.' });
    }

    // Check expiry
    if (pending.expiresAt < new Date() && ['pending', 'calling'].includes(pending.status)) {
      pending.status = 'expired';
      await pending.save();
    }

    // Poll Exotel call status if we have a callSid and transfer is still in progress
    let callStatus = null;
    if (pending.callSid && ['pending', 'calling'].includes(pending.status)) {
      callStatus = await getCallStatus(pending.callSid);
      if (callStatus) {
        // Update status based on Exotel call result
        if (['completed'].includes(callStatus.status)) {
          // Call was answered and completed — mark as confirmed (waiting for user action in UI)
          pending.status = 'confirmed';
          await pending.save();
        } else if (['no-answer', 'busy', 'failed', 'canceled'].includes(callStatus.status)) {
          pending.status = 'expired';
          await pending.save();
        }
      }
    }

    let newBalance = null;
    if (pending.status === 'completed') {
      const acc = await Account.findOne({ userId: req.userId });
      if (acc) newBalance = acc.balance;
    }

    res.json({
      id: pending._id,
      status: pending.status,
      amount: pending.amount,
      receiverAccount: pending.receiverAccount,
      beneficiaryName: pending.beneficiaryName,
      riskLevel: pending.riskLevel,
      riskReason: pending.riskReason,
      newBalance,
      createdAt: pending.createdAt,
    });
  } catch (error) {
    res.status(500).json({ message: 'Server error.', error: error.message });
  }
};
