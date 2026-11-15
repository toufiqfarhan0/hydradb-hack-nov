"""
Unified Production Runner for Render Free Service Deployment
Spawns FastAPI backend on internal port 8000 and Next.js frontend on Render $PORT.
Enables complete end-to-end deployment within a single Render Free Web Service.
"""
import os
import sys
import time
import subprocess
import signal
import urllib.request

def wait_for_backend(url: str, timeout_sec: int = 15):
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            with urllib.request.urlopen(url, timeout=1) as res:
                if res.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

def run():
    render_port = os.environ.get("PORT", "3000")
    internal_api_port = "8000"

    print("=======================================================")
    print("  LUCEN — UNIFIED PRODUCTION RUNNER (RENDER DEPLOYMENT)")
    print(f"  Public External Port:  {render_port}")
    print(f"  Internal FastAPI Port: {internal_api_port}")
    print("=======================================================")

    # 1. Start FastAPI backend
    fastapi_env = os.environ.copy()
    fastapi_env["PORT"] = internal_api_port
    fastapi_cmd = [
        sys.executable, "-m", "uvicorn", "backend.server:app",
        "--host", "127.0.0.1", "--port", internal_api_port
    ]
    print(f"[RUNNER] Starting FastAPI: {' '.join(fastapi_cmd)}")
    p_backend = subprocess.Popen(fastapi_cmd, env=fastapi_env)

    # Wait for FastAPI health check
    health_url = f"http://127.0.0.1:{internal_api_port}/api/health"
    print(f"[RUNNER] Waiting for backend readiness on {health_url}...")
    ready = wait_for_backend(health_url)
    if ready:
        print("[RUNNER] FastAPI backend is ready.")
    else:
        print("[RUNNER] Warning: FastAPI health check timed out; continuing with Next.js startup.")

    # 2. Start Next.js frontend on external Render $PORT
    web_dir = os.path.join(os.path.dirname(__file__), "web")
    next_env = os.environ.copy()
    next_env["PORT"] = render_port
    next_env["BACKEND_URL"] = f"http://127.0.0.1:{internal_api_port}"

    is_win = sys.platform.startswith("win")
    npm_cmd = "npm.cmd" if is_win else "npm"
    next_cmd = [npm_cmd, "run", "start"]

    print(f"[RUNNER] Starting Next.js frontend on port {render_port}...")
    p_frontend = subprocess.Popen(next_cmd, cwd=web_dir, env=next_env)

    def shutdown(signum, frame):
        print("\n[RUNNER] Received termination signal. Shutting down gracefully...")
        p_frontend.terminate()
        p_backend.terminate()
        p_frontend.wait()
        p_backend.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Monitor frontend process
    exit_code = p_frontend.wait()
    p_backend.terminate()
    sys.exit(exit_code)

if __name__ == "__main__":
    run()
