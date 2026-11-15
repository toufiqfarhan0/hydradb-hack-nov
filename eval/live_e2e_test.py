"""
Lucen Live End-to-End Verification Test Suite
Tests live running FastAPI server on http://localhost:8000
Validates all endpoints, HydraDB GraphBLAS traversal, SlateDB/MinIO status,
OpenCypher query generation, token reduction benchmarks, and continual learning updates.
"""
import sys
import json
import time
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"

def log_header(title: str):
    print(f"\n[TEST SUITE] {title}")
    print("-" * 65)

def get_json(endpoint: str):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={"User-Agent": "Lucen-E2E-Verifier"})
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200 OK from {endpoint}, got {res.status}"
        return json.loads(res.read().decode())

def post_json(endpoint: str, payload: dict):
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Lucen-E2E-Verifier"}
    )
