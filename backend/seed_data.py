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
        properties={"channel_id": "C08A91KL2", "topic": "Live P0/P1 Outages and Incident Mitigation", "tier": "P0"},
        confidence=1.0
    ),
    EntityNode(
        id="ent_github_hotfix_pr",
        name="GitHub PR #842 (Fix connection pool leak)",
        entity_type="PullRequest",
        properties={"repo": "hydra-corp/core-api", "pr_number": 842, "branch": "fix/db-pool-exhaustion", "status": "draft"},
        confidence=0.95
    ),
    EntityNode(
        id="ent_aws_rds_instance",
        name="AWS RDS 'hydra-aurora-prod'",
        entity_type="CloudResource",
        properties={"arn": "arn:aws:rds:us-east-1:991283:cluster:hydra-aurora-prod", "region": "us-east-1", "engine": "aurora-postgresql"},
        confidence=0.98
    ),
    EntityNode(
        id="ent_sentry_issue_id",
        name="Sentry Issue #ERR-9104 (PoolTimeout: queue full)",
        entity_type="TelemetryIssue",
        properties={"issue_id": "ERR-9104", "events_24h": 4120, "first_seen": "12 mins ago", "culprit": "db.connection_pool.get_connection"},
        confidence=0.97
    ),
    EntityNode(
        id="ent_linear_p0_ticket",
        name="Linear Ticket #ENG-3921",
        entity_type="ProjectTicket",
        properties={"ticket_id": "ENG-3921", "title": "P0: Connection Pool Exhaustion in US-East-1", "priority": "Urgent"},
        confidence=1.0
    ),
    EntityNode(
        id="ent_docker_worker_service",
        name="Docker Container 'hydra-worker-api-4'",
        entity_type="ContainerInstance",
        properties={"container_id": "a918f0cb18a2", "image": "hydra/api:v3.1.2", "status": "unhealthy (OOM alert)"},
        confidence=0.94
    )
]

TOOLS = [
    # PostgreSQL Tools
    ToolNode(
        id="tool_pg_slow_queries",
        name="pg_inspect_slow_queries",
        server_id="mcp_postgres",
        description="Returns top 10 running queries sorted by execution duration and lock wait time from pg_stat_activity",
        parameters_schema={"type": "object", "properties": {"limit": {"type": "integer", "default": 10}, "min_duration_ms": {"type": "integer", "default": 500}}},
        estimated_token_cost=420
    ),
    ToolNode(
        id="tool_pg_explain_analyze",
        name="pg_explain_query_plan",
        server_id="mcp_postgres",
        description="Generates EXPLAIN (ANALYZE, BUFFERS) execution plan for suspect SQL query to identify seq scans",
        parameters_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        estimated_token_cost=460
    ),
    ToolNode(
        id="tool_pg_terminate_pid",
        name="pg_terminate_backend_pid",
        server_id="mcp_postgres",
        description="Gracefully cancels or kills stuck Postgres PID holding exclusive table locks",
        parameters_schema={"type": "object", "properties": {"pid": {"type": "integer"}, "grace_seconds": {"type": "integer", "default": 5}}, "required": ["pid"]},
        estimated_token_cost=390
    ),
    ToolNode(
        id="tool_pg_pool_metrics",
        name="pg_check_connection_pool",
        server_id="mcp_postgres",
        description="Queries PgBouncer or native connection pool utilization, idle timeouts, and waiting clients",
        parameters_schema={"type": "object", "properties": {"pool_name": {"type": "string"}}},
        estimated_token_cost=380
    ),

    # Slack Tools
    ToolNode(
        id="tool_slack_post_incident",
        name="slack_post_incident_bulletin",
        server_id="mcp_slack",
        description="Broadcasts structured P0/P1 incident alert to targeted war-room channel with live updates",
        parameters_schema={"type": "object", "properties": {"channel": {"type": "string"}, "severity": {"type": "string"}, "summary": {"type": "string"}}, "required": ["channel", "severity", "summary"]},
        estimated_token_cost=480
    ),
    ToolNode(
        id="tool_slack_page_oncall",
        name="slack_page_oncall_engineer",
        server_id="mcp_slack",
        description="Initiates urgent PagerDuty/Slack emergency ping to the designated primary rotation lead",
        parameters_schema={"type": "object", "properties": {"team": {"type": "string"}, "incident_summary": {"type": "string"}}, "required": ["team", "incident_summary"]},
        estimated_token_cost=440
    ),
    ToolNode(
        id="tool_slack_thread_update",
        name="slack_append_thread_update",
        server_id="mcp_slack",
        description="Appends technical diagnosis or fix status to existing incident thread without notifying entire org",
        parameters_schema={"type": "object", "properties": {"thread_ts": {"type": "string"}, "body": {"type": "string"}}, "required": ["thread_ts", "body"]},
        estimated_token_cost=410
    ),

    # GitHub Tools
    ToolNode(
        id="tool_gh_create_pr",
        name="github_create_pull_request",
        server_id="mcp_github",
        description="Opens hotfix PR against main branch with changelog description and reviewer assignment",
        parameters_schema={"type": "object", "properties": {"repo": {"type": "string"}, "branch": {"type": "string"}, "title": {"type": "string"}, "body": {"type": "string"}}, "required": ["repo", "branch", "title"]},
        estimated_token_cost=510
    ),
    ToolNode(
        id="tool_gh_get_diff",
        name="github_inspect_commit_diff",
        server_id="mcp_github",
        description="Fetches raw git diff of target commit or branch to isolate introduced code regression",
        parameters_schema={"type": "object", "properties": {"repo": {"type": "string"}, "ref": {"type": "string"}}, "required": ["repo", "ref"]},
        estimated_token_cost=450
    ),
    ToolNode(
        id="tool_gh_merge_pr",
        name="github_merge_pull_request",
        server_id="mcp_github",
        description="Triggers auto-merge (squash or rebase) once all CI checks and approvals pass",
        parameters_schema={"type": "object", "properties": {"repo": {"type": "string"}, "pr_number": {"type": "integer"}}, "required": ["repo", "pr_number"]},
        estimated_token_cost=420
    ),

    # AWS Tools
    ToolNode(
        id="tool_aws_rds_metrics",
        name="aws_fetch_rds_metrics",
        server_id="mcp_aws",
        description="Retrieves CloudWatch CPUUtilization, DatabaseConnections, and FreeableMemory over last 60 minutes",
        parameters_schema={"type": "object", "properties": {"instance_id": {"type": "string"}, "period_minutes": {"type": "integer"}}, "required": ["instance_id"]},
        estimated_token_cost=470
    ),
    ToolNode(
        id="tool_aws_ecs_restart",
        name="aws_restart_ecs_service",
        server_id="mcp_aws",
        description="Forces new deployment of ECS service with zero-downtime rolling container replacement",
        parameters_schema={"type": "object", "properties": {"cluster": {"type": "string"}, "service": {"type": "string"}}, "required": ["cluster", "service"]},
        estimated_token_cost=490
    ),

    # Sentry Tools
    ToolNode(
        id="tool_sentry_get_stacktrace",
        name="sentry_fetch_issue_stacktrace",
        server_id="mcp_sentry",
        description="Retrieves full unminified stacktrace, culprit line, and local environment variables for issue ID",
        parameters_schema={"type": "object", "properties": {"issue_id": {"type": "string"}}, "required": ["issue_id"]},
        estimated_token_cost=440
    ),
    ToolNode(
        id="tool_sentry_resolve_issue",
        name="sentry_mark_issue_resolved",
        server_id="mcp_sentry",
        description="Marks Sentry crash issue as resolved in current release build to verify error rate decay",
        parameters_schema={"type": "object", "properties": {"issue_id": {"type": "string"}, "release": {"type": "string"}}, "required": ["issue_id"]},
        estimated_token_cost=390
    ),
