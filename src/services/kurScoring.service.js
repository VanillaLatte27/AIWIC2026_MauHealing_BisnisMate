/**
 * KUR Bankability Scoring & Bank Dossier Generator
 * Partner Banks: Bank Mandiri, Bank BRI, BPD Bali
 */

class KurScoringService {
  getScore() {
    return {
      merchant_id: "WS-0902-BALI",
      merchant_name: "Warung Bu Wayan Sudarmi",
      aggregate_score: 88.5,
      max_score: 100,
      status: "Tier 1 - Sangat Layak (Pre-Approved KUR Mikro)",
      recommended_ceiling_idr: 75000000,
      interest_rate_subsidy: "6% p.a. (KUR Pemerintah)",
      dimensions: [
        { name: "Kelengkapan SAK EMKM", score: 95, benchmark: 65, status: "Unggul" },
        { name: "Rasio Arus Kas (DSCR)", score: 88, benchmark: 60, status: "2.85x Aman" },
        { name: "Pemisahan Kas Adat/Pribadi", score: 82, benchmark: 55, status: "Terkontrol" },
        { name: "Frekuensi Transaksi Digital", score: 92, benchmark: 60, status: "Aktif QRIS" },
        { name: "Ketahanan Siklus Stok Adat", score: 86, benchmark: 50, status: "Tahan Galungan" }
      ],
      partner_banks: [
        { bank: "Bank Mandiri", status: "Host-to-Host Ready", dossier_format: "OJK_Mandiri_v2.pdf" },
        { bank: "Bank BRI", status: "Host-to-Host Ready", dossier_format: "BRI_KUR_Dossier.pdf" },
        { bank: "Bank BPD Bali", status: "Host-to-Host Ready", dossier_format: "BPD_Bali_KreditKrama.pdf" }
      ]
    };
  }

  generateDossier() {
    return {
      status: "generated",
      dossier_id: `KUR-MDR-2026-${Date.now().toString().slice(-4)}`,
      merchant_name: "Warung Bu Wayan Sudarmi",
      target_bank: "Bank Mandiri (Penyalur KUR UMKM)",
      pre_approved_limit: "Rp 75.000.000",
      validity: "30 Hari ke Depan",
      compliance_seal: "SAK EMKM IAI & UU PDP Terenkripsi",
      download_ready: true
    };
  }
}

module.exports = new KurScoringService();
