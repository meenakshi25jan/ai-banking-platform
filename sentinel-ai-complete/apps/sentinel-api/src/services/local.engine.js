import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '../../../../');

function getValue(obj, dotted) {
  return dotted.split('.').reduce((acc, key) => acc?.[key], obj);
}

function compare(left, operator, right) {
  if (operator === '>') return left > right;
  if (operator === '>=') return left >= right;
  if (operator === '<') return left < right;
  if (operator === '<=') return left <= right;
  if (operator === '===') return left === right;
  return false;
}

async function loadPolicy(journey) {
  const policyPath = path.join(repoRoot, 'shared', 'policies', `${journey}.v1.json`);
  const raw = await fs.readFile(policyPath, 'utf8');
  return JSON.parse(raw);
}

function evaluateFraud(context) {
  const amount = Number(context.input.amount || 0);
  const monthlyIncome = Number(context.input.monthlyIncome || 0);
  const crossBorder = Boolean(context.input.crossBorder);
  const failedAttempts = Number(context.input.failedAttemptsLast24h || 0);
  let score = 0.12;
  const reasons = [];
  if (amount >= 100000) { score += 0.5; reasons.push('High-value transfer'); }
  if (amount >= 25000) { score += 0.12; reasons.push('Elevated transfer amount'); }
  if (crossBorder) { score += 0.2; reasons.push('Cross-border activity'); }
  if (failedAttempts >= 5) { score += 0.25; reasons.push('Repeated failed attempts'); }
  if (monthlyIncome > 0 && amount >= monthlyIncome * 2) { score += 0.2; reasons.push('Amount significantly exceeds stated income'); }
  return { name: 'fraud', score: Math.min(score, 1), modelVersion: 'local-fraud-rules-v2', reasons };
}

function evaluateIntent(context) {
  const purpose = String(context.input.purpose || context.input.message || '').toLowerCase();
  let score = 0.08;
  const reasons = [];
  for (const token of ['urgent', 'immediately', 'now', 'emergency', 'asap']) {
    if (purpose.includes(token)) {
      score += 0.18;
      reasons.push(`High-pressure language detected: ${token}`);
    }
  }
  if (context.journey === 'assistant' && /password|otp|cvv|pin/.test(purpose)) {
    score += 0.35;
    reasons.push('Sensitive credential-seeking pattern detected');
  }
  return { name: 'intent', score: Math.min(score, 1), modelVersion: 'local-intent-rules-v2', reasons };
}

function evaluateBehavior(context) {
  let score = 0.1;
  const reasons = [];
  if (context.input.newDevice) { score += 0.65; reasons.push('New device detected'); }
  if (!context.input.deviceId) { score += 0.08; reasons.push('Missing device identifier'); }
  if (context.input.ipAddress && context.input.geo && String(context.input.geo).toLowerCase() === 'unknown') {
    score += 0.1;
    reasons.push('Unknown geolocation provided');
  }
  return { name: 'behavior', score: Math.min(score, 1), modelVersion: 'local-behavior-rules-v2', reasons };
}

function evaluateCompliance(context) {
  const amount = Number(context.input.amount || 0);
  const loanAmount = Number(context.input.loanAmount || 0);
  let score = 0.95;
  const reasons = [];
  if (context.input.crossBorder) { score -= 0.25; reasons.push('Cross-border compliance review required'); }
  if (amount >= 200000 || loanAmount >= 500000) { score -= 0.3; reasons.push('High-value threshold compliance check'); }
  if (context.journey === 'assistant' && context.input.channel === 'public') {
    score -= 0.2;
    reasons.push('Public channel requires stricter content controls');
  }
  return { name: 'compliance', score: Math.max(score, 0), modelVersion: 'local-compliance-rules-v2', reasons };
}

function evaluateUrgency(context) {
  const combined = String(context.input.purpose || context.input.message || '').toLowerCase();
  let score = 0.05;
  const reasons = [];
  for (const token of ['urgent', 'immediately', 'now', 'emergency', 'asap']) {
    if (combined.includes(token)) {
      score += 0.18;
      reasons.push(`Urgency language detected: ${token}`);
    }
  }
  if (context.input.expediteRequested) {
    score += 0.2;
    reasons.push('Customer requested expedited handling');
  }
  return { name: 'urgency', score: Math.min(score, 1), modelVersion: 'local-urgency-rules-v1', reasons };
}

function calculateTrustScore(signals) {
  const fraud = signals.fraud?.score ?? 0;
  const intent = signals.intent?.score ?? 0;
  const behavior = signals.behavior?.score ?? 0;
  const urgency = signals.urgency?.score ?? 0;
  const compliance = signals.compliance?.score ?? 1;
  const trust = (1 - fraud) * 30 + (1 - intent) * 15 + (1 - behavior) * 20 + (1 - urgency) * 10 + compliance * 25;
  return Math.max(0, Math.min(100, Math.round(trust)));
}

function evaluatePolicy(policy, signals) {
  const sorted = [...policy.rules].sort((a, b) => b.priority - a.priority);
  for (const rule of sorted) {
    const left = getValue(signals, rule.field);
    if (compare(left, rule.operator, rule.value)) {
      return {
        decision: rule.decision,
        reason: rule.reason,
        ruleId: rule.id,
        policyVersion: policy.version,
      };
    }
  }
  return {
    decision: 'ALLOW',
    reason: 'No blocking or review policy triggered',
    ruleId: 'default-allow',
    policyVersion: policy.version,
  };
}

function buildSignals(context) {
  const base = {
    behavior: evaluateBehavior(context),
    compliance: evaluateCompliance(context),
  };

  if (['transfer', 'login', 'loan'].includes(context.journey)) {
    base.fraud = evaluateFraud(context);
  }

  if (['transfer', 'assistant', 'loan'].includes(context.journey)) {
    base.intent = evaluateIntent(context);
  }

  if (['transfer', 'assistant'].includes(context.journey)) {
    base.urgency = evaluateUrgency(context);
  }

  return base;
}

export async function runLocalDecision(context) {
  const signals = buildSignals(context);
  const policy = await loadPolicy(context.journey);
  const policyResult = evaluatePolicy(policy, signals);
  const trustScore = calculateTrustScore(signals);
  const reasons = [...new Set([policyResult.reason, ...Object.values(signals).flatMap((signal) => signal.reasons || [])])];
  return {
    traceId: randomUUID(),
    signals,
    policyResult,
    decision: {
      journey: context.journey,
      actor: context.actor,
      decision: policyResult.decision,
      trustScore,
      reasons,
      policyVersion: policyResult.policyVersion,
      ruleId: policyResult.ruleId,
      createdAt: new Date().toISOString(),
    },
  };
}
