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

class EntityNode(BaseModel):
    id: str
    name: str
    entity_type: str  # e.g., 'DatabaseConnection', 'SlackChannel', 'GitBranch', 'AWSRegion', 'APICredential'
    properties: Dict[str, Any]
    resolved_at_task: Optional[str] = None
    confidence: float = 1.0

class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str  # 'BELONGS_TO', 'PROVIDES', 'REQUIRES_ENTITY', 'RESOLVES_ENTITY', 'PREFERS'
    weight: float = 1.0
    properties: Dict[str, Any] = Field(default_factory=dict)

class TraversalRequest(BaseModel):
    task: str
    preloaded_entities: Optional[List[str]] = Field(default_factory=list)
    mode: str = "lucen_graph"  # "lucen_graph" or "naive_preload"
    top_k_tools: int = 4

class TraversalStep(BaseModel):
    step_num: int
    stage: str
    opencypher_fragment: str
    matched_nodes: List[str]
    description: str

class TraversalResult(BaseModel):
    task: str
    mode: str
    engine_mode: str = "local_csr_fallback"
    selected_tools: List[ToolNode]
    resolved_entities: List[EntityNode]
    subgraph_nodes: List[Dict[str, Any]]
    subgraph_edges: List[Dict[str, Any]]
    opencypher_query: str
    tokens_used: int
    baseline_tokens: int
    token_reduction_pct: float
    estimated_cost_saved_pct: float
    traversal_latency_ms: float
    explanation: str
    steps: List[TraversalStep]

class FeedbackRequest(BaseModel):
    task: str
    tool_id: str
    success: bool
    latency_ms: Optional[float] = None

class PipelineStage(BaseModel):
    stage_index: int
    stage_name: str
    tool_id: str
    tool_name: str
    server_id: str
    description: str
    input_bindings: Dict[str, Any]
    output_schema: Dict[str, Any]
    upstream_dependencies: List[str]
    handoff_type: str

class PipelineResult(BaseModel):
    task: str
    pipeline_type: str
    stages: List[PipelineStage]
    total_stages: int
    dataflow_links: List[Dict[str, Any]]
    pre_bound_entities: List[Dict[str, Any]]
    total_tokens: int
    baseline_tokens: int
    token_reduction_pct: float
    traversal_latency_ms: float
    dag_status: str
    notes: Optional[str] = None

class BenchmarkMetric(BaseModel):
    task_name: str
    domain: str
    naive_tokens: int
    lucen_tokens: int
    reduction_pct: float
    naive_latency_ms: float
    lucen_latency_ms: float
    accuracy_improvement_pct: float
    tools_isolated: int
    total_tools_available: int
