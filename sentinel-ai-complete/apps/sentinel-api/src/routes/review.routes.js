import { Router } from 'express';
import { requireAuth, requireReviewer } from '../middleware/auth.middleware.js';
import { getReviewQueue, assignReview, resolveReview } from '../controllers/review.controller.js';

const router = Router();
router.get('/queue', requireAuth, requireReviewer, getReviewQueue);
router.post('/:id/assign', requireAuth, requireReviewer, assignReview);
router.post('/:id/resolve', requireAuth, requireReviewer, resolveReview);
export { router as reviewRouter };
