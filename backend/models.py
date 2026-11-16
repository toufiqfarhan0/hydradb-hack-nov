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
    mutating: bool = False
    destructive: bool = False
    allowed_environments: List[str] = Field(default_factory=lambda: ["development", "staging", "production"])
    schema_hash: Optional[str] = None
    secret_handles: Dict[str, str] = Field(default_factory=dict)
    reads_private_data: bool = False
    external_facing: bool = False
    data_classification: str = "INTERNAL"  # 'PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED'

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
    environment: str = "production"  # 'production', 'staging', 'development'
    allow_destructive: bool = False
    sampling_mode: str = "thompson"  # 'thompson', 'mean', 'greedy'

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
    environment: str = "production"
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
    security_enforced: bool = True
    pruned_for_security: List[str] = Field(default_factory=list)
    tamper_alerts: List[Dict[str, Any]] = Field(default_factory=list)
    secret_handles_bound: int = 0
    bandit_sampling: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    task: str
    tool_id: str
    success: bool
    latency_ms: Optional[float] = None
    capability_id: Optional[str] = None

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

class FallbackRequest(BaseModel):
    tool_id: str
    error_reason: str = "connection_refused"
    target_entity: Optional[str] = None

class FallbackResult(BaseModel):
    original_tool_id: str
    original_tool_name: str
    error_reason: str
    fallback_tool_id: str
    fallback_tool_name: str
    server_id: str
    recovery_action: str
    failover_entity: Dict[str, Any]
    traversal_latency_ms: float
    cypher_query: str
    auto_recovered: bool
    status: str

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

class SecurityAuditResult(BaseModel):
    total_tools_audited: int
    destructive_tools_identified: int
    mutating_tools_identified: int
    production_blocked_tools: List[str]
    tamper_verified: bool
    tampered_tools_detected: List[str]
    prompt_injection_alerts: List[Dict[str, str]]
    secret_handles_configured: int
    policy_status: str

class IngestRequest(BaseModel):
    source_type: str = "claude_config"  # 'claude_config', 'json_manifest', 'live_server'
    config_path: Optional[str] = None
    manifest_data: Optional[Dict[str, Any]] = None
    server_command: Optional[str] = None

class IngestResult(BaseModel):
    status: str
    servers_ingested: int
    tools_ingested: int
    capabilities_generated: int
    entities_extracted: int
    edges_created: int
    server_names: List[str]
    schema_hashes_registered: int
    ingest_latency_ms: float

class BlastRadiusResult(BaseModel):
    tool_id: str
    tool_name: str
    action_type: str  # 'DESTRUCTIVE', 'MUTATING', 'READ_ONLY'
    target_entities: List[Dict[str, Any]]
    dependent_tools_affected: List[Dict[str, Any]]
    downstream_chained_tools: List[str]
    affected_environments: List[str]
    impacted_services: List[str] = Field(default_factory=list)
    data_assets_at_risk: List[str] = Field(default_factory=list)
    risk_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    blast_summary: str
    requires_human_approval: bool

class ExpandRequest(BaseModel):
    current_tools: List[str]
    task_context: Optional[str] = ""
    expand_depth: int = 1

class ExpandResult(BaseModel):
    original_tools: List[str]
    expanded_tools: List[ToolNode]
    expansion_rationale: str
    expansion_latency_ms: float

