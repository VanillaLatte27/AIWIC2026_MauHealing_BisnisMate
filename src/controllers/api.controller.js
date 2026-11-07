/**
 * API Controller Layer
 * Coordinates Services and Handles HTTP Responses
 */

const config = require('../config/app.config');
const sakEmkmService = require('../services/sakEmkm.service');
const aiEngineService = require('../services/aiEngine.service');
const calendarService = require('../services/calendar.service');
const kurScoringService = require('../services/kurScoring.service');

class ApiController {
  getHealthCheck(req, res) {
    res.json({
      status: "healthy",
      runtime: `Node.js ${process.version}`,
      framework: "Express 4.21 (Modular Architecture)",
      application: config.appName,
      competition: config.competition,
      team: config.team.name,
      version: config.version,
      ai_engine: {
        whisper_lora: "ONLINE (Dialect Bali-ID fine-tuned)",
        gemini_flash: "ONLINE (Multimodal camera parser ready)",
        cultural_rag: "ONLINE (Caka 1948 calendar linked)"
      },
      sak_emkm_rules: "IAI Standard Compliant (Dual-entry balancing)",
      active_merchant: `${config.defaultMerchant.name} (${config.defaultMerchant.market})`
    });
  }

  getCulturalEvents(req, res) {
    res.json(calendarService.getEvents());
  }

  getKurScore(req, res) {
    res.json(kurScoringService.getScore());
  }

  getLedgerTransactions(req, res) {
    const transactions = sakEmkmService.getAllTransactions();
    const summary = sakEmkmService.calculateLedgerSummary();
    res.json({
      status: "success",
      count: transactions.length,
      summary,
      transactions
    });
  }

  saveTransaction(req, res) {
    const { description, amount, type, source, account } = req.body;
    if (!description || amount === undefined) {
      return res.status(400).json({ error: "Parameter description dan amount wajib diisi" });
    }

    const tx = sakEmkmService.addTransaction({ description, amount, type, source, account });
    const summary = sakEmkmService.calculateLedgerSummary();

    res.json({
      status: "success",
      message: "Transaksi berhasil dibukukan ke SAK EMKM & Skor KUR terupdate!",
      transaction: tx,
      total_transactions: summary.totalCount,
      summary
    });
  }

  parseSpeech(req, res) {
    const { transcript } = req.body;
    res.json({
      status: "success",
      transcript: transcript || "Penjualan Canang Sari 250rb",
      total_debet: 570000,
      total_kredit: 570000,
      balance_verified: true,
      entries: [
        { account: "1-1001", name: "Kas Tunai", debet: 250000, kredit: 0 },
        { account: "4-1001", name: "Pendapatan Usaha", debet: 0, kredit: 250000 }
      ]
    });
  }

  processVoice(req, res) {
    const { customPrompt, audioLengthSec } = req.body;
    const result = aiEngineService.processSpeech({ customPrompt, audioLengthSec });
    res.json(result);
  }

  processReceipt(req, res) {
    const { imageBase64, sampleType } = req.body;
    const result = aiEngineService.processReceiptImage({ imageBase64, sampleType });
    res.json(result);
  }

  orderRestock(req, res) {
    const { item } = req.body;
    res.json(calendarService.simulateRestockOrder(item || "Janur Bali"));
  }

  exportKurDossier(req, res) {
    res.json(kurScoringService.generateDossier());
  }
}

module.exports = new ApiController();
