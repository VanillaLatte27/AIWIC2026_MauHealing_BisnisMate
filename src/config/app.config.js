/**
 * BisnisMate Application Configuration
 * Artificial Intelligence World Innovation Challenge (AIWIC) 2026
 * Team: Mau Healing
 */

module.exports = {
  appName: "BisnisMate Web",
  version: "4.2.0-aiwic2026",
  competition: "AIWIC 2026",
  team: {
    name: "Mau Healing",
    leader: "Candra Kus Khoiri Wicaksono",
    role: "Inovator & AI Engineer",
    institution: "Bank Indonesia Partner / Independent Team",
    repository: "https://github.com/candrak/AIWIC2026_MauHealing_BisnisMate"
  },
  server: {
    port: process.env.PORT || 3000,
    corsOrigin: "*"
  },
  defaultMerchant: {
    id: "WS-0902-BALI",
    name: "Warung Bu Wayan Sudarmi",
    market: "Pasar Kumbasari Denpasar",
    cluster: "Sembako & Canang Sari",
    since: "2018",
    qrisStatus: "Active (Bank Indonesia KPw Bali)"
  },
  aiSpecs: {
    whisperLora: {
      model: "Whisper-large-v3-lora-balinese-v2",
      wer: "5.8%",
      latencyMs: 680,
      supportedDialects: ["Bali Alus", "Bali Madia", "Indonesia Pasar", "Campuran Bali-ID"]
    },
    geminiVision: {
      model: "Gemini-2.5-Flash-Vision-Parser",
      f1Score: "94.2%",
      latencyMs: 620,
      supportedInputs: ["Nota Tulis Tangan", "Bon Kertas Basah", "Faktur Distributor Grosir"]
    },
    calendarRag: {
      ontology: "Kalender Bali Saka (Caka 1948)",
      database: "Bali Cultural & Tourism Knowledge Graph",
      forecastWindowDays: 14
    }
  }
};
