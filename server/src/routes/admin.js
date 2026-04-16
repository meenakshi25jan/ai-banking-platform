const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const admin = require('../middleware/admin');
const adminController = require('../controllers/adminController');
const aiController = require('../controllers/aiController');

// All routes require auth + admin
router.use(auth, admin);

router.get('/dashboard', adminController.getDashboardStats);
router.get('/users', adminController.getAllUsers);
router.get('/bank-balance', adminController.getBankBalance);
router.post('/add-balance', adminController.addBalance);
router.post('/add-balance-bulk', adminController.addBalanceBulk);
router.post('/withdraw-to-account', aiController.adminWithdrawToUser);
router.get('/held-accounts', adminController.getHeldAccounts);
router.post('/held-accounts/:accountId/unhold', adminController.unholdAccount);
router.get('/governance-reviews', adminController.getGovernanceReviews);
router.post('/governance-reviews/:reviewId/resolve', adminController.resolveGovernanceReview);

module.exports = router;
