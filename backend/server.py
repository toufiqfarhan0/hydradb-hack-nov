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
