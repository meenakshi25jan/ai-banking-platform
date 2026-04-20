import { createReviewRecord } from '../repositories/review.repository.js';

export async function createReviewCase({ decisionId, summary, priority = 'HIGH' }) {
  return createReviewRecord({ decisionId, summary, priority });
}
