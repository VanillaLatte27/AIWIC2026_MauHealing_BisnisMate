/**
 * BisnisMate Web MVP — Node.js Production Server Entrypoint
 * Artificial Intelligence World Innovation Challenge (AIWIC) 2026
 * Team: Mau Healing
 * Product: BisnisMate (Autonomous Financial & Inventory Co-Pilot Web Platform)
 * 
 * Usage:
 *   npm start   (or: node server.js [port])
 */

const app = require('./src/app');
const config = require('./src/config/app.config');

const PORT = process.env.PORT || process.argv[2] || config.server.port || 3000;

const server = app.listen(PORT, () => {
  console.log("============================================================");
  console.log("🚀 BisnisMate Web MVP (Modular Node.js Architecture) LIVE!");
  console.log(`📍 URL: http://localhost:${PORT}`);
  console.log(`🏆 Competition: ${config.competition} | Team: '${config.team.name}'`);
  console.log(`👤 Leader / Innovator: ${config.team.leader}`);
  console.log(`📂 Node.js Version: ${process.version}`);
  console.log("⚡ REST API Endpoints:");
  console.log("   - GET  /api/v1/health-check");
  console.log("   - POST /api/v1/process-voice");
  console.log("   - POST /api/v1/process-receipt");
  console.log("   - GET  /api/v1/ledger-transactions");
  console.log("   - POST /api/v1/save-transaction");
  console.log("   - GET  /api/v1/cultural-events");
  console.log("   - GET  /api/v1/kur-score");
  console.log("============================================================");
});

module.exports = server;
