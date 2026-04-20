import { getReviewCases, updateReviewCase } from '../repositories/review.repository.js';

export async function getReviewQueue(_req, res, next) {
  try {
    const items = await getReviewCases();
    res.json({ items });
  } catch (error) {
    next(error);
  }
}

export async function assignReview(req, res, next) {
  try {
    const updated = await updateReviewCase(req.params.id, {
      assignedTo: req.auth.sub,
      status: 'IN_PROGRESS'
    });
    if (!updated) return res.status(404).json({ error: 'Review case not found' });
    res.json(updated);
  } catch (error) {
    next(error);
  }
}

export async function resolveReview(req, res, next) {
  try {
    const updated = await updateReviewCase(req.params.id, {
      status: req.body.status || 'RESOLVED',
      resolution: req.body.resolution || 'Reviewer completed case',
      resolvedBy: req.auth.sub,
      resolvedAt: new Date().toISOString()
    });
    if (!updated) return res.status(404).json({ error: 'Review case not found' });
    res.json(updated);
  } catch (error) {
    next(error);
  }
}
