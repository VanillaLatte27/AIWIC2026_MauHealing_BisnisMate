/**
 * BisnisMate Web MVP — Node.js Automated Test Suite
 * AIWIC 2026 Submission - Team Mau Healing
 */

const http = require('http');
const { spawn } = require('child_process');

console.log("============================================================");
console.log("🧪 Running BisnisMate Node.js MVP Automated Verification Suite...");
console.log("============================================================");

// Spawn server on port 3099 for automated testing
const serverProcess = spawn('node', ['server.js', '3099'], {
  cwd: __dirname,
  stdio: 'inherit'
});

setTimeout(async () => {
  try {
    // Helper function for GET requests
    function httpGet(path) {
      return new Promise((resolve, reject) => {
        http.get(`http://localhost:3099${path}`, (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => resolve({ status: res.statusCode, data: JSON.parse(data) }));
        }).on('error', reject);
      });
    }

    // Helper function for POST requests
    function httpPost(path, body) {
      return new Promise((resolve, reject) => {
        const payload = JSON.stringify(body);
        const req = http.request(`http://localhost:3099${path}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
          }
        }, (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => resolve({ status: res.statusCode, data: JSON.parse(data) }));
        });
        req.on('error', reject);
        req.write(payload);
        req.end();
      });
    }

    // Test 1: Health Check
    const res1 = await httpGet('/api/v1/health-check');
    if (res1.status === 200 && res1.data.status === 'healthy') {
      console.log("  [PASS] Test 1: Health Check API (Node.js/Express) -> 200 OK");
    } else {
      throw new Error("Test 1 Failed");
    }

    // Test 2: Cultural Events
    const res2 = await httpGet('/api/v1/cultural-events');
    if (res2.status === 200 && res2.data.events.length >= 2) {
      console.log(`  [PASS] Test 2: Cultural Calendar API -> Loaded ${res2.data.events.length} festivals`);
    } else {
      throw new Error("Test 2 Failed");
    }

    // Test 3: KUR Score
    const res3 = await httpGet('/api/v1/kur-score');
    if (res3.status === 200 && res3.data.aggregate_score > 80) {
      console.log(`  [PASS] Test 3: KUR Bankability Score API -> Score ${res3.data.aggregate_score} (Tier 1)`);
    } else {
      throw new Error("Test 3 Failed");
    }

    // Test 4: Multimodal Speech Parsing (Balance Check)
    const res4 = await httpPost('/api/v1/parse-speech', { transcript: "Laku 50 tanding canang sari 250rb tunai" });
    if (res4.status === 200 && res4.data.balance_verified === true) {
      console.log(`  [PASS] Test 4: SAK EMKM Balance Engine -> Balanced (${res4.data.total_debet} = ${res4.data.total_kredit})`);
    } else {
      throw new Error("Test 4 Failed");
    }

    // Test 5: Save Transaction to Ledger
    const res5 = await httpPost('/api/v1/save-transaction', {
      description: "Penjualan Dupa Harum",
      amount: 45000,
      type: "income"
    });
    if (res5.status === 200 && res5.data.status === 'success') {
      console.log(`  [PASS] Test 5: Live SAK EMKM Ledger Update -> ${res5.data.message}`);
    } else {
      throw new Error("Test 5 Failed");
    }

    console.log("============================================================");
    console.log("🎉 ALL 5/5 NODE.JS TEST SUITES PASSED WITH 100% SUCCESS!");
    console.log("============================================================");
    serverProcess.kill();
    process.exit(0);

  } catch (err) {
    console.error("❌ Test failed:", err);
    serverProcess.kill();
    process.exit(1);
  }
}, 1500);
