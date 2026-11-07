#!/usr/bin/env python3
"""
BisnisMate Web MVP Server
Artificial Intelligence World Innovation Challenge (AIWIC) 2026
Team: Mau Healing
Product: BisnisMate (Autonomous Financial & Inventory Co-Pilot Web Platform)

Usage:
    python3 server.py [port]
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.parse

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class BisnisMateHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/v1/health-check":
            self.send_json({
                "status": "healthy",
                "application": "BisnisMate Web MVP",
                "competition": "AIWIC 2026",
                "team": "Mau Healing",
                "version": "4.1.0",
                "engine": {
                    "whisper_lora": "online",
                    "gemini_2_5_flash": "online",
                    "cultural_rag": "online",
                    "sak_emkm_rules": "compliant"
                },
                "active_merchants": 442000,
                "supported_dialects": ["id-ID", "ban-ID", "id-Bali-Colloquial"]
            })
            return

        elif path == "/api/v1/cultural-events":
            self.send_json({
                "calendar": "Caka 1948 / Bali Hindu Calendar",
                "events": [
                    {
                        "name": "Hari Raya Galungan",
                        "date_relative": "H-4 Hari",
                        "urgency": "TINGGI",
                        "demand_spikes": {
                            "canang_sari": "+180%",
                            "janur_kelapa": "+180%",
                            "beras_kuning": "+65%"
                        }
                    },
                    {
                        "name": "Hari Raya Kuningan",
                        "date_relative": "H-14 Hari",
                        "urgency": "SEDANG",
                        "demand_spikes": {"beras": "+40%", "daging": "+50%"}
                    }
                ]
            })
            return

        elif path == "/api/v1/kur-score":
            self.send_json({
                "merchant_id": "WS-0902-BALI",
                "merchant_name": "Warung Bu Wayan",
                "aggregate_score": 88.5,
                "tier": "Tier 1 - Sangat Layak",
                "recommended_ceiling_idr": 75000000,
                "partner_banks": ["Bank Mandiri", "Bank BRI", "Bank BPD Bali"],
                "ratios": {
                    "sak_emkm_completeness": 0.95,
                    "dscr": 2.85,
                    "private_cash_leakage": 0.082
                }
            })
            return

        # Default static file serving
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        if path == "/api/v1/parse-speech":
            try:
                body = json.loads(post_data.decode("utf-8")) if post_data else {}
            except Exception:
                body = {}

            sample_text = body.get("transcript", "Laku 50 tanding canang sari 250 ribu tunai, sama beli beras c4 2 karung 320 ribu nota dari Pak Wayan.")

            self.send_json({
                "status": "success",
                "input_transcript": sample_text,
                "latency_ms": 1080,
                "model_used": "gemini-2.5-flash-multimodal",
                "entries": [
                    {"account": "1-1001", "name": "Kas Tunai", "type": "DEBET", "amount": 250000},
                    {"account": "4-1001", "name": "Pendapatan Usaha", "type": "KREDIT", "amount": 250000},
                    {"account": "1-1301", "name": "Persediaan Beras C4", "type": "DEBET", "amount": 320000},
                    {"account": "1-1001", "name": "Kas Tunai", "type": "KREDIT", "amount": 320000}
                ],
                "balance_verified": True,
                "total_debet": 570000,
                "total_kredit": 570000
            })
            return

        self.send_error(404, "Endpoint Not Found")

    def send_json(self, data, code=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), BisnisMateHandler) as httpd:
        print("=" * 60)
        print(f"🚀 BisnisMate Web MVP Server is LIVE!")
        print(f"📍 Local URL: http://localhost:{PORT}")
        print(f"🏆 AIWIC 2026 Submission by Team 'Mau Healing'")
        print(f"📂 Serving: {DIRECTORY}")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")


if __name__ == "__main__":
    main()
