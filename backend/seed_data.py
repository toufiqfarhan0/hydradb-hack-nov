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
