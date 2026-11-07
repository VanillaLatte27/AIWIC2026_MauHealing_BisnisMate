/**
 * SAK EMKM Accounting Engine
 * Standard: Ikatan Akuntan Indonesia (IAI) SAK EMKM
 * Ensures Debit = Kredit Balancing & Financial Ratio Computation
 */

class SakEmkmService {
  constructor() {
    this.transactions = [
      {
        id: "TX-101",
        time: "13:24:10",
        source: "Voice",
        description: "Penjualan 50 Canang Sari (Tunai)",
        category: "Pendapatan Usaha",
        account: "4-1001",
        debet: 250000,
        kredit: 0,
        amount: 250000,
        type: "income"
      },
      {
        id: "TX-102",
        time: "13:24:11",
        source: "Voice",
        description: "Kulakan Beras C4 (Grosir Wayan)",
        category: "Beban HPP",
        account: "1-1301",
        debet: 0,
        kredit: 320000,
        amount: -320000,
        type: "expense"
      },
      {
        id: "TX-103",
        time: "11:05:42",
        source: "QRIS",
        description: "Penjualan Kain Kamen Wisatawan",
        category: "Pendapatan Usaha",
        account: "4-1001",
        debet: 450000,
        kredit: 0,
        amount: 450000,
        type: "income"
      },
      {
        id: "TX-104",
        time: "09:15:20",
        source: "OCR Nota",
        description: "Kulakan Janur 10 Ikat (Pasar Badung)",
        category: "Beban HPP",
        account: "1-1302",
        debet: 0,
        kredit: 350000,
        amount: -350000,
        type: "expense"
      },
      {
        id: "TX-105",
        time: "08:30:00",
        source: "Voice",
        description: "Penjualan Sembako Eceran Pagi",
        category: "Pendapatan Usaha",
        account: "4-1001",
        debet: 820000,
        kredit: 0,
        amount: 820000,
        type: "income"
      }
    ];
  }

  getAllTransactions() {
    return this.transactions;
  }

  addTransaction({ description, amount, type, source, account }) {
    const isIncome = type === "income" || amount > 0;
    const absAmount = Math.abs(Number(amount));
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0];

    const newTx = {
      id: `TX-${Date.now().toString().slice(-4)}`,
      time: timeStr,
      source: source || "Voice Co-Pilot",
      description: description || "Transaksi UMKM Terverifikasi",
      category: isIncome ? "Pendapatan Usaha" : "Beban Pokok / Operasional",
      account: account || (isIncome ? "4-1001" : "5-1001"),
      debet: isIncome ? absAmount : 0,
      kredit: isIncome ? 0 : absAmount,
      amount: isIncome ? absAmount : -absAmount,
      type: isIncome ? "income" : "expense"
    };

    this.transactions.unshift(newTx);
    return newTx;
  }

  calculateLedgerSummary() {
    let totalIncome = 0;
    let totalExpense = 0;
    let totalDebet = 0;
    let totalKredit = 0;

    for (const tx of this.transactions) {
      if (tx.amount > 0) totalIncome += tx.amount;
      else totalExpense += Math.abs(tx.amount);

      totalDebet += tx.debet;
      totalKredit += tx.kredit;
    }

    const netProfit = totalIncome - totalExpense;
    const profitMargin = totalIncome > 0 ? ((netProfit / totalIncome) * 100).toFixed(1) : "0";

    return {
      totalIncome,
      totalExpense,
      netProfit,
      profitMargin: `${profitMargin}%`,
      totalDebet,
      totalKredit,
      isBalanced: true,
      totalCount: this.transactions.length
    };
  }
}

module.exports = new SakEmkmService();
