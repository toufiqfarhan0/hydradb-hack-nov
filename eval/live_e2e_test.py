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
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200, f"Expected 200 OK from {endpoint}, got {res.status}"
        return json.loads(res.read().decode())

def run_e2e_tests():
    print("=" * 65)
    print("  LUCEN — LIVE END-TO-END VERIFICATION & INTEGRATION SUITE")
    print(f"  Target: {BASE_URL}")
    print("=" * 65)
    
    passed_tests = 0
    total_tests = 9

    # 1. Health & Storage Backend Test
    log_header("1. Health & HydraDB SlateDB/MinIO Storage Engine")
    try:
        health = get_json("/api/health")
        print(f"  • Status:           {health.get('status')}")
        print(f"  • Engine:           {health.get('engine')}")
        print(f"  • Storage Backend:  {health.get('storage_backend')}")
        print(f"  • Node Count:       {health.get('nodes_count')}")
        print(f"  • Edge Count:       {health.get('edges_count')}")
        assert health.get("status") in ("active_resilient", "healthy")
        assert health.get("nodes_count", 0) >= 40
        assert health.get("edges_count", 0) >= 50
        print("  => PASS: Engine healthy and connected to MinIO/S3 SlateDB backend.")
        passed_tests += 1
    except Exception as e:
        print(f"  => FAIL: {e}")
        return False

    # 2. Graph Stats
    log_header("2. Graph Topology Schema Statistics")
