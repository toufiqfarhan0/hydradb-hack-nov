"""
Lucen Seed Dataset - Real-world Enterprise MCP Ecosystem, Tools, and Context Entities
"""
from typing import Dict, List, Any
from backend.models import MCPServerNode, ToolNode, CapabilityNode, EntityNode, GraphEdge

MCP_SERVERS = [
    MCPServerNode(
        id="mcp_postgres",
        name="PostgreSQL Inspector",
        description="Live inspection, slow query EXPLAIN analysis, table schemas, and connection pool health",
        version="2.4.0",
        transport="stdio"
    ),
    MCPServerNode(
        id="mcp_slack",
        name="Slack Enterprise",
        description="Post alerts to incident channels, thread replies, user paging, and incident announcements",
        version="1.8.2",
        transport="sse"
    ),
    MCPServerNode(
        id="mcp_github",
        name="GitHub Repo Manager",
        description="Repository inspection, Pull Request creation, commit diffs, reviews, and git branch workflows",
        version="3.1.0",
        transport="stdio"
    ),
    MCPServerNode(
        id="mcp_aws",
        name="AWS Cloud Ops",
        description="RDS metrics, ECS task definitions, CloudWatch alarms, and S3 bucket policies",
        version="2.0.1",
        transport="stdio"
    ),
    MCPServerNode(
