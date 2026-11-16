# Reuse Policy, Attributions & Architectural Boundaries

This document discloses all third-party libraries, protocols, external services, and intellectual dependencies utilized in Lucen, along with architectural boundaries.

---

## 1. Hackathon Eligibility & Original Authorship

Lucen was built from scratch for **the HydraDB Hackathon** (Track 2: The Agent Context Layer). 

All core logic in this repository:
- GraphBLAS sparse matrix semiring traversal engine (`backend/hydradb_engine.py`)
- Runtime entity pre-binding and disambiguation logic
- Drop-in Model Context Protocol (MCP) JSON-RPC Gateway (`backend/mcp_gateway.py`)
- Live Gemini function-calling agent harness (`tools/gemini_agent.py`)
- Swiss Modernist Web UI & Matrix Visualizer (`web/`)
- Benchmark and evaluation test harnesses (`eval/`)

was developed specifically for this hackathon submission.

---

## 2. Reused Open-Source Libraries & Frameworks

| Component | License | Role in Lucen | Modification / Customization |
|---|---|---|---|
| **HydraDB** | AGPL-3.0 | Target graph database engine supporting OpenCypher & GraphBLAS | Interfaced via HTTP client and local embedded CSR fallback engine |
| **Model Context Protocol (MCP)** | MIT | Open standard for tool and resource communication | Implemented standard stdio JSON-RPC 2.0 gateway server |
| **FastAPI / Uvicorn** | MIT / BSD | Internal REST API and traversal endpoint backend | Custom route handlers for graph traversal, verification, and live agent invocations |
| **Next.js 15 (React 19)** | MIT | Frontend UI, Matrix visualizer, and live console | Custom Swiss Modernist design system, Zero external UI component libraries |
| **Tailwind CSS 4** | MIT | Utility-first CSS styling | Custom architectural typographic scales and monochromatic palettes |
| **NumPy / SciPy** | BSD-3-Clause | Sparse matrix computation (`scipy.sparse.csr_matrix`) | Powers in-memory CSR matrix semiring traversal verification |
| **Google Gemini API** | Commercial / Free Tier | Live autonomous AI coding agent verification | Function-calling integration via REST endpoints in `tools/gemini_agent.py` |

---

## 3. Synthetic vs Real Infrastructure Tools

In enterprise incident simulations:
- Certain database hosts (e.g. `pg-cluster-prod.internal:5432`) and container endpoints are simulated runtime targets to provide safe, reproducible evaluation across test environments.
- In `backend/mcp_gateway.py`, simulated tools are explicitly labeled with `"simulated": true` and `"transport": "mock_upstream"` to ensure total academic and operational transparency.
- Local SQLite query tools execute real in-memory SQL execution against live SQLite engines.
- The Google Gemini agent integration (`tools/gemini_agent.py`) executes **real, live API calls** against Google's Gemini models (`gemini-flash-lite-latest` / `gemini-3.5-flash-lite`).
