"""
Lucen Backend Server - FastAPI Application for HydraDB Agent Context Layer
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import TraversalRequest, TraversalResult, FeedbackRequest
from backend.hydradb_engine import HydraDBContextEngine

app = FastAPI(
    title="Lucen - HydraDB Agent Context Layer",
    description="Live context store for autonomous agents: tools, skills, MCP definitions, and resolved entities via OpenCypher",
    version="1.0.0"
)

# Enable CORS for local dev and embedded frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = HydraDBContextEngine()

@app.get("/api/health")
async def health():
    return await engine.check_health()

@app.get("/api/graph/stats")
async def get_graph_stats():
    return {
        "servers": len(engine.servers),
        "tools": len(engine.tools),
        "capabilities": len(engine.capabilities),
        "entities": len(engine.entities),
        "edges": len(engine.edges),
        "iterations_logged": len(engine.iteration_history),
        "current_accuracy": engine.iteration_history[-1]["accuracy_pct"],
        "token_reduction_pct": engine.iteration_history[-1]["token_reduction_pct"]
    }

@app.get("/api/graph/data")
async def get_graph_data():
    return engine.get_full_graph()

@app.post("/api/traverse", response_model=TraversalResult)
async def traverse_graph(req: TraversalRequest):
    try:
        return engine.traverse(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def post_feedback(req: FeedbackRequest):
    return engine.record_feedback(req)

@app.get("/api/benchmark")
async def get_benchmark_suite():
    benchmarks = engine.get_benchmarks()
    return {
        "suite": benchmarks,
        "summary": {
            "avg_reduction_pct": round(sum(b.reduction_pct for b in benchmarks) / len(benchmarks), 1),
            "avg_latency_reduction_ms": round(sum(b.naive_latency_ms - b.lucen_latency_ms for b in benchmarks) / len(benchmarks), 1),
            "avg_accuracy_gain_pct": round(sum(b.accuracy_improvement_pct for b in benchmarks) / len(benchmarks), 1)
        }
    }

@app.get("/api/learning-curve")
async def get_learning_curve():
    return engine.iteration_history

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Lucen - HydraDB Agent Context Layer",
        "version": "1.0.0",
        "engine": "SuiteSparse GraphBLAS 9.3 + SlateDB",
        "web_ui": "http://localhost:3000",
        "api_docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.server:app", host="0.0.0.0", port=port, reload=False)
