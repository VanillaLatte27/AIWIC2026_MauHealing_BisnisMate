/**
 * REST API Routes Configuration
 * Endpoints for AI, SAK EMKM Ledger, Cultural Calendar, and KUR Scoring
 */

const express = require('express');
const router = express.Router();
const apiController = require('../controllers/api.controller');

// System Health & Specs
router.get('/health-check', apiController.getHealthCheck);

// Multimodal AI Pipelines (Voice & Camera OCR)
router.post('/parse-speech', apiController.parseSpeech);
router.post('/process-voice', apiController.processVoice);
router.post('/process-receipt', apiController.processReceipt);

// SAK EMKM Accounting Ledger
router.get('/ledger-transactions', apiController.getLedgerTransactions);
router.post('/save-transaction', apiController.saveTransaction);

// Cultural Calendar & Adat Restock Alerts
router.get('/cultural-events', apiController.getCulturalEvents);
router.post('/order-restock', apiController.orderRestock);

// Bank KUR Scoring & Dossier
router.get('/kur-score', apiController.getKurScore);
router.get('/export-kur-dossier', apiController.exportKurDossier);

module.exports = router;
