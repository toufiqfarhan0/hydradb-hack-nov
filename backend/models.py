"""
Lucen Data Models - Graph Node & Edge Definitions for Agent Context Layer
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class MCPServerNode(BaseModel):
    id: str
    name: str
    description: str
    version: str = "1.0.0"
    transport: str = "stdio"
    status: str = "active"

class ToolNode(BaseModel):
    id: str
    name: str
    server_id: str
    description: str
    parameters_schema: Dict[str, Any]
    estimated_token_cost: int = Field(default=350, description="Tokens to serialize full schema into LLM prompt")
    invocation_count: int = 0
    avg_latency_ms: float = 120.0

class CapabilityNode(BaseModel):
    id: str
    name: str
    domain: str
    keywords: List[str]

