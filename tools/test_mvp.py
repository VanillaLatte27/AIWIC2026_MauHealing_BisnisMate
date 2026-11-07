#!/usr/bin/env python3
"""
BisnisMate Web MVP Automated Test Suite
AIWIC 2026 Submission - Team Mau Healing
"""

import sys
import json
import urllib.request
import urllib.error
import subprocess
import time

def test_endpoints():
    print("=" * 60)
    print("🧪 Running BisnisMate Web MVP Automated Verification Suite...")
    print("=" * 60)

    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(base_dir, "server.py")
    proc = subprocess.Popen([sys.executable, server_script, "8089"], cwd=base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1.5)

    try:
        # Test 1: Health Check
        url = "http://localhost:8089/api/v1/health-check"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            assert data["status"] == "healthy"
            print("  [PASS] Test 1: Health Check API (200 OK) -> System is healthy")

        # Test 2: Cultural Events
        url = "http://localhost:8089/api/v1/cultural-events"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            assert len(data["events"]) >= 2
            print("  [PASS] Test 2: Cultural Calendar Sync API -> Events loaded")

        # Test 3: KUR Score
        url = "http://localhost:8089/api/v1/kur-score"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            assert data["aggregate_score"] > 80
            print(f"  [PASS] Test 3: KUR Bankability Score API -> Score {data['aggregate_score']} (Tier 1)")

        # Test 4: Multimodal Speech Parsing POST
        url = "http://localhost:8089/api/v1/parse-speech"
        payload = json.dumps({"transcript": "Laku 50 tanding canang sari 250rb tunai"}).encode()
        post_req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(post_req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            assert data["balance_verified"] is True
            assert data["total_debet"] == data["total_kredit"]
            print(f"  [PASS] Test 4: SAK EMKM Balance Engine -> Balanced ({data['total_debet']} = {data['total_kredit']})")

        # Test 5: Static Index File
        url = "http://localhost:8089/index.html"
        with urllib.request.urlopen(url, timeout=5) as resp:
            html = resp.read().decode()
            assert "BisnisMate" in html
            assert "Mau Healing" in html
            print("  [PASS] Test 5: Web UI Frontend Delivered (HTML5, Tailwind, Chart.js)")

        print("=" * 60)
        print("🎉 ALL 5/5 MVP FUNCTIONALITY TESTS PASSED (100% SUCCESS)!")
        print("=" * 60)
        return True

    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    success = test_endpoints()
    sys.exit(0 if success else 1)
