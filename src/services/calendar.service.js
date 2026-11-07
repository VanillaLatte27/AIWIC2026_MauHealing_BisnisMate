/**
 * Balinese Cultural Calendar & Inventory Prediction Service
 * Caka 1948 Sacred Calendar & Tourism Events
 */

class CalendarService {
  getEvents() {
    return {
      calendar: "Caka 1948 / Bali Hindu Sacred Calendar",
      current_sasih: "Kadasa",
      events: [
        {
          id: "EVT-01",
          name: "Hari Raya Galungan",
          date_relative: "H-4 Hari",
          balinese_date: "Buda Kliwon Dungulan",
          urgency: "TINGGI",
          spikes: [
            { item: "Janur & Kelapa Daksina", percentage: "+180%", alert: "Rawan langka mulai H-2" },
            { item: "Bunga Gumitir & Canang Sari", percentage: "+220%", alert: "Kebutuhan harian naik 3x lipat" },
            { item: "Beras C4 & Beras Kuning", percentage: "+65%", alert: "Pola konsumsi tumpeng meningkat" }
          ],
          restock_advice: "Lakukan kulakan janur & beras sekarang sebelum kenaikan harga distributor besok lusa."
        },
        {
          id: "EVT-02",
          name: "Hari Raya Kuningan",
          date_relative: "H-14 Hari",
          balinese_date: "Saniscara Kliwon Kuningan",
          urgency: "SEDANG",
          spikes: [
            { item: "Beras Ketan & Janur Pilihan", percentage: "+50%", alert: "Perayaan 10 hari pasca Galungan" }
          ]
        },
        {
          id: "EVT-03",
          name: "Pesta Kesenian Bali (PKB)",
          date_relative: "Bulan Depan",
          balinese_date: "Taman Budaya Art Center",
          urgency: "EVENT WISATA",
          spikes: [
            { item: "Kain Kamen & Souvenir Lokal", percentage: "+90%", alert: "Arus wisatawan domestik melonjak" }
          ]
        }
      ]
    };
  }

  simulateRestockOrder(item) {
    return {
      status: "success",
      message: `Pesanan restock otomatis untuk [${item}] telah dikirimkan ke Paguyuban Distributor Pasar Badung.`,
      estimated_delivery: "Besok Pagi Pukul 05.30 WITA",
      payment_method: "Talangan Kas SAK EMKM / Tempo 3 Hari"
    };
  }
}

module.exports = new CalendarService();
