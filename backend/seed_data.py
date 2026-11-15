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
        id="mcp_sentry",
        name="Sentry Telemetry",
        description="Real-time crash stacktraces, unhandled exceptions, error grouping, and affected user metrics",
        version="1.3.5",
        transport="stdio"
    ),
    MCPServerNode(
        id="mcp_docker",
        name="Docker Container Runtime",
        description="Inspect running containers, stream stderr logs, trigger zero-downtime rolling restarts",
        version="1.9.0",
        transport="stdio"
    ),
    MCPServerNode(
        id="mcp_linear",
        name="Linear Issue Tracker",
        description="Create urgent incident tickets, link GitHub PRs, assign engineering owners, update cycles",
        version="2.1.0",
        transport="sse"
    ),
    MCPServerNode(
        id="mcp_brave",
        name="Brave Search Engine",
        description="Live external web query, official documentation retrieval, and known CVE vulnerability search",
        version="1.1.0",
        transport="stdio"
    )
]

CAPABILITIES = [
    CapabilityNode(id="cap_db_diagnostics", name="Database Diagnostics", domain="infrastructure", keywords=["database", "postgres", "slow query", "lock", "connection pool", "replica", "deadlock"]),
    CapabilityNode(id="cap_incident_alerting", name="Incident Alerting", domain="collaboration", keywords=["slack", "channel", "page", "alert", "notify", "war room", "announcement", "oncall"]),
    CapabilityNode(id="cap_code_review", name="Code Review & PR", domain="development", keywords=["github", "pull request", "pr", "commit", "diff", "branch", "git", "review"]),
    CapabilityNode(id="cap_cloud_telemetry", name="Cloud Metrics & Autoscaling", domain="infrastructure", keywords=["aws", "rds", "cloudwatch", "cpu", "memory", "ecs", "alarm", "metrics"]),
    CapabilityNode(id="cap_error_tracking", name="Exception Stacktrace Analysis", domain="observability", keywords=["sentry", "error", "exception", "crash", "stacktrace", "unhandled", "500"]),
    CapabilityNode(id="cap_container_mgmt", name="Container Lifecycle", domain="infrastructure", keywords=["docker", "container", "restart", "logs", "oomkill", "healthcheck"]),
    CapabilityNode(id="cap_issue_tracking", name="Project & Issue Tracking", domain="project", keywords=["linear", "ticket", "issue", "bug", "triage", "sprint", "milestone"]),
    CapabilityNode(id="cap_cve_research", name="Security & CVE Research", domain="security", keywords=["cve", "vulnerability", "patch", "exploit", "search", "docs", "advisory"]),
    CapabilityNode(id="cap_schema_migration", name="Schema Migration & DDL", domain="database", keywords=["migration", "alter table", "create index", "schema", "ddl"]),
    CapabilityNode(id="cap_access_revocation", name="Access Control & Secrets", domain="security", keywords=["revoke", "credential", "api key", "token", "iam", "rotate", "permission"])
]

ENTITIES = [
    EntityNode(
        id="ent_db_prod_replica",
        name="Production DB Primary & Read Replica",
        entity_type="DatabaseCluster",
        properties={"host": "pg-cluster-prod.internal:5432", "database": "hydra_analytics", "max_connections": 400, "current_connections": 387},
        confidence=0.99
    ),
    EntityNode(
        id="ent_slack_war_room",
        name="Slack #incident-critical-ops",
        entity_type="SlackChannel",
