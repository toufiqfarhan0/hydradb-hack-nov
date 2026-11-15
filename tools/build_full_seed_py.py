import os
import json

def build():
    from generate_catalog import generate_catalog
    servers_raw, tool_verbs = generate_catalog()

    out_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "seed_data.py"))

    # Servers
    servers_code = []
    for s_id, s_name, s_desc, s_trans, s_ver in servers_raw:
        servers_code.append(
            f"    MCPServerNode(id='{s_id}', name='{s_name}', description='{s_desc}', transport='{s_trans}', version='{s_ver}'),"
        )

    # Specific signature tools for key scenarios to maintain 100% backward compatibility
    core_tools_by_server_verb = {
        ("mcp_postgres", "check_connection_pool"): ("pg_check_connection_pool", "Queries PgBouncer or native connection pool utilization, idle timeouts, and waiting clients", 380, "cap_db_diagnostics", "entity_pg_cluster_prod"),
        ("mcp_postgres", "inspect_health"): ("pg_explain_slow_query", "Executes EXPLAIN (ANALYZE, BUFFERS) on heavy queries causing CPU spikes", 420, "cap_db_slow_queries", "entity_pg_cluster_prod"),
        ("mcp_postgres", "fetch_metrics"): ("pg_inspect_table_bloat", "Calculates dead tuple bloat and autovacuum starvation thresholds", 360, "cap_db_diagnostics", "entity_pg_cluster_prod"),
        ("mcp_postgres", "drain_traffic"): ("pg_kill_idle_in_transaction", "Safely terminates idle-in-transaction sessions blocking table locks", 340, "cap_db_connection_pool", "entity_pg_cluster_prod"),
        ("mcp_slack", "dispatch_alert"): ("slack_post_incident_bulletin", "Publishes formatted incident cards to incident channel with active status and responder pings", 410, "cap_incident_alerting", "entity_slack_incident_room"),
        ("mcp_slack", "verify_configuration"): ("slack_update_incident_status", "Updates incident severity level, commander on call, and customer impact summary", 390, "cap_incident_alerting", "entity_slack_incident_room"),
        ("mcp_github", "trigger_restart"): ("github_create_pull_request", "Opens hotfix PR against main branch with changelog description and reviewer assignment", 510, "cap_pr_management", "entity_github_pr_842"),
        ("mcp_github", "stream_logs"): ("github_fetch_commit_diff", "Inspects git diff of recent merges to pinpoint regression culprits", 430, "cap_git_diff", "entity_github_pr_842"),
        ("mcp_docker", "stream_logs"): ("docker_stream_container_logs", "Streams recent stderr logs from designated container ID with error grep filtering", 420, "cap_container_logs", "entity_docker_container"),
        ("mcp_docker", "trigger_restart"): ("docker_restart_container", "Triggers graceful container rolling restart with zero traffic drops", 390, "cap_container_restart", "entity_docker_container"),
        ("mcp_sentry", "stream_logs"): ("sentry_fetch_issue_stacktrace", "Retrieves complete Python/Go/TypeScript stacktrace with culprit commit attribution", 480, "cap_crash_telemetry", "entity_sentry_issue"),
        ("mcp_aws_rds", "fetch_metrics"): ("aws_fetch_rds_metrics", "Retrieves Aurora/RDS CPU, FreeableMemory, and ReadIOPS metrics across 60-second intervals", 440, "cap_cloud_metrics", "entity_aws_rds_primary"),
        ("mcp_redis", "fetch_metrics"): ("redis_inspect_eviction_spikes", "Monitors key eviction spikes and cache hit ratio drops", 370, "cap_cache_diagnostics", "entity_redis_cache"),
        ("mcp_linear", "dispatch_alert"): ("linear_create_incident_issue", "Creates urgent engineering task in Linear linked to active Slack incident", 430, "cap_incident_alerting", "entity_linear_issue"),
        ("mcp_datadog", "stream_logs"): ("datadog_query_apm_traces", "Queries distributed trace waterfall for service response latency degradation", 460, "cap_apm_tracing", "entity_datadog_apm"),
        ("mcp_k8s", "stream_logs"): ("k8s_describe_crashing_pod", "Queries kubectl describe pod for OOMKilled events and liveness probe failures", 450, "cap_k8s_ops", "entity_k8s_pod"),
        ("mcp_k8s", "drain_traffic"): ("k8s_drain_failing_node", "Safely cordons and drains Kubernetes node experiencing memory pressure", 490, "cap_k8s_ops", "entity_k8s_pod"),
        ("mcp_vault", "verify_configuration"): ("vault_renew_database_lease", "Renews expiring dynamic Postgres database credentials lease in HashiCorp Vault", 410, "cap_security_vault", "entity_vault_lease"),
        ("mcp_brave", "inspect_health"): ("brave_search_cve_advisories", "Searches official CVE security databases and GitHub advisory bulletin for vulnerabilities", 470, "cap_cve_search", "entity_cve_advisory")
    }

    # Generate 500 Tools (10 per server)
    tools_code = []
    edges_code = []
    
    tool_counter = 0
    all_tool_ids = []

    # Capabilities definitions
    domain_map = {
        "mcp_postgres": "Database Diagnostics",
        "mcp_mysql": "Database Diagnostics",
        "mcp_redis": "Cache & Performance",
        "mcp_clickhouse": "OLAP Analytics",
        "mcp_snowflake": "Data Warehouse",
        "mcp_bigquery": "Data Warehouse",
        "mcp_mongodb": "Document Database",
        "mcp_elasticsearch": "Search & Indexing",
        "mcp_kafka": "Message Streaming",
        "mcp_rabbitmq": "Message Queues",
        "mcp_aws": "Cloud Infrastructure",
        "mcp_aws_rds": "Database Diagnostics",
        "mcp_aws_lambda": "Serverless Compute",
        "mcp_aws_ecs": "Container Lifecycle",
        "mcp_k8s": "Container Lifecycle",
        "mcp_docker": "Container Lifecycle",
        "mcp_terraform": "Infrastructure as Code",
        "mcp_cloudflare": "Edge & Networking",
        "mcp_datadog": "Observability & APM",
        "mcp_splunk": "Log Analytics",
        "mcp_sentry": "Crash Telemetry",
        "mcp_grafana": "Observability & APM",
        "mcp_prometheus": "Observability & APM",
        "mcp_pagerduty": "Incident Response",
        "mcp_newrelic": "Observability & APM",
        "mcp_honeycomb": "Distributed Tracing",
        "mcp_github": "Code & Version Control",
        "mcp_gitlab": "CI/CD Automation",
        "mcp_linear": "Incident Response",
        "mcp_jira": "Incident Response",
        "mcp_argocd": "GitOps Deployment",
        "mcp_circleci": "CI/CD Automation",
        "mcp_snyk": "Security & Vulnerability",
        "mcp_sonarqube": "Code Quality",
        "mcp_vault": "Security & Secrets",
        "mcp_aws_iam": "Security & Secrets",
        "mcp_okta": "Identity & Access",
        "mcp_fastly": "Edge & Networking",
        "mcp_wireguard": "Edge & Networking",
        "mcp_nginx": "Edge & Networking",
        "mcp_slack": "Incident Response",
        "mcp_discord": "Communications",
        "mcp_notion": "Documentation & Runbooks",
        "mcp_confluence": "Documentation & Runbooks",
        "mcp_oncall": "Incident Response",
        "mcp_stripe": "Billing & Financial",
        "mcp_twilio": "Alerts & Notifications",
        "mcp_sendgrid": "Alerts & Notifications",
        "mcp_brave": "External Research",
        "mcp_perplexity": "External Research"
    }

    # Generate 100 Capabilities
    capabilities_dict = {
        "cap_db_diagnostics": ("Database Diagnostics", "Database Diagnostics", ["postgres", "mysql", "database", "query", "pool", "deadlock", "table"]),
        "cap_db_connection_pool": ("Connection Pool Health", "Database Diagnostics", ["pool", "pgbouncer", "connections", "max_connections", "exhaustion"]),
        "cap_db_slow_queries": ("Slow Query Profiling", "Database Diagnostics", ["slow", "explain", "analyze", "vacuum", "index", "cpu"]),
        "cap_cache_diagnostics": ("Cache Eviction & Hit Ratio", "Cache & Performance", ["redis", "cache", "eviction", "memory", "fragmentation"]),
        "cap_incident_alerting": ("Incident Alerting & Broadcast", "Incident Response", ["alert", "incident", "slack", "pagerduty", "channel", "war room", "critical"]),
        "cap_container_logs": ("Container Stderr/Stdout Streaming", "Container Lifecycle", ["container", "docker", "k8s", "pod", "logs", "stderr", "oom"]),
        "cap_container_restart": ("Graceful Container Restart", "Container Lifecycle", ["restart", "docker", "rolling", "reboot", "bounce"]),
        "cap_crash_telemetry": ("Exception Stacktrace Analysis", "Crash Telemetry", ["sentry", "crash", "stacktrace", "unhandled", "exception", "error"]),
        "cap_pr_management": ("Hotfix Pull Request Lifecycle", "Code & Version Control", ["github", "pr", "pull request", "branch", "merge", "hotfix"]),
        "cap_git_diff": ("Commit Blame & Regression Diffs", "Code & Version Control", ["diff", "blame", "commit", "git", "regression", "culprit"]),
        "cap_cloud_metrics": ("Cloud Infrastructure Metrics", "Cloud Infrastructure", ["aws", "rds", "ec2", "cloudwatch", "metrics", "iops", "cpu"]),
        "cap_k8s_ops": ("Kubernetes Pod & Node Lifecycle", "Container Lifecycle", ["k8s", "pod", "node", "drain", "crashloop", "kubectl", "ingress"]),
        "cap_security_vault": ("Secrets Lease & Token Renewal", "Security & Secrets", ["vault", "secret", "lease", "credential", "token", "password"]),
        "cap_cve_search": ("Security Advisory & CVE Search", "Security & Vulnerability", ["cve", "vulnerability", "patch", "advisory", "security", "exploit"]),
        "cap_apm_tracing": ("Distributed APM Waterfall Traces", "Observability & APM", ["apm", "trace", "datadog", "waterfall", "span", "latency"]),
        "cap_log_analytics": ("Enterprise SPL Log Aggregation", "Log Analytics", ["splunk", "logs", "aggregation", "index", "queries", "grep"]),
        "cap_streaming_kafka": ("Kafka Consumer Partition Offsets", "Message Streaming", ["kafka", "consumer", "topic", "partition", "lag", "offsets"]),
        "cap_queue_deadletter": ("RabbitMQ Dead-Letter Management", "Message Queues", ["rabbitmq", "queue", "unacked", "deadletter", "ack", "churn"]),
        "cap_gitops_argocd": ("GitOps Manifest Synchronization", "GitOps Deployment", ["argocd", "gitops", "sync", "manifest", "drift", "rollback"]),
        "cap_ci_pipelines": ("CI/CD Parallel Pipeline Healing", "CI/CD Automation", ["gitlab", "circleci", "pipeline", "job", "retry", "build"]),
        "cap_billing_audit": ("Stripe Financial Audit & Disputes", "Billing & Financial", ["stripe", "billing", "charge", "refund", "subscription", "dispute"]),
        "cap_dns_edge": ("Cloudflare DNS & Edge WAF Rules", "Edge & Networking", ["cloudflare", "dns", "waf", "edge", "rate limit", "ddos"])
    }

    # Add remaining domain capabilities to reach 100
    for i in range(len(capabilities_dict) + 1, 101):
        c_id = f"cap_spec_{i}"
        domain_choice = list(domain_map.values())[i % len(domain_map)]
        capabilities_dict[c_id] = (f"Operational Capability #{i}", domain_choice, [f"domain_{i}", f"spec_{i}", "enterprise", "telemetry"])

    # 80 Bound Entities
    entities_dict = {
        "entity_pg_cluster_prod": ("Production DB Primary & Read Replica", "DatabaseCluster", {"host": "pg-cluster-prod.internal:5432", "database": "hydra_analytics", "max_connections": 400, "current_connections": 387, "region": "us-east-1"}),
        "entity_pg_cluster_stage": ("Staging PostgreSQL Cluster", "DatabaseCluster", {"host": "pg-stage.internal:5432", "database": "hydra_stage", "max_connections": 100, "current_connections": 12, "region": "us-east-1"}),
        "entity_slack_incident_room": ("Slack #incident-critical-ops", "SlackChannel", {"channel_id": "C09283741", "workspace": "HydraCorp Enterprise", "incident_lead": "@oncall_infra", "active_incident": "INC-8812"}),
        "entity_slack_devex_room": ("Slack #devex-alerts", "SlackChannel", {"channel_id": "C09283799", "workspace": "HydraCorp Enterprise", "incident_lead": "@devex_bot", "active_incident": "NONE"}),
        "entity_github_pr_842": ("GitHub PR #842 (Fix connection pool leak)", "PullRequest", {"repo": "hydra-corp/core-api", "pr_number": 842, "branch": "fix/db-pool-exhaustion", "status": "draft", "author": "agent-copilot"}),
        "entity_docker_container": ("Docker core-api-gateway-c8f9", "DockerContainer", {"container_id": "c8f921ab01e4", "image": "hydra-corp/core-api:v2.14.0", "status": "oom_killed", "exit_code": 137}),
        "entity_aws_rds_primary": ("AWS Aurora RDS Primary Instance", "RDSInstance", {"arn": "arn:aws:rds:us-east-1:9928172:db:hydra-primary", "instance_class": "db.r6g.4xlarge", "cpu_utilization": 94.2}),
        "entity_sentry_issue": ("Sentry Issue #5021 (DeadlockDetected)", "SentryIssue", {"issue_id": "ERR-5021", "first_seen_commit": "e4f8b91", "events_24h": 14200, "impacted_users": 840}),
        "entity_redis_cache": ("Redis Session & Rate-Limit Cache", "RedisInstance", {"endpoint": "redis-prod.internal:6379", "used_memory": "14.2GB", "max_memory": "16.0GB", "evicted_keys_rate": "420/s"}),
        "entity_linear_issue": ("Linear INC-492 (Core API Outage)", "LinearIssue", {"issue_id": "INC-492", "priority": "Urgent", "team": "Platform Infra", "cycle": "Active"}),
        "entity_datadog_apm": ("Datadog APM Service: Core-API", "DatadogService", {"service_name": "core-api-prod", "p99_latency_ms": 1820.0, "apdex_score": 0.42}),
        "entity_k8s_pod": ("Kubernetes Pod: api-worker-7b94", "KubernetesPod", {"namespace": "production", "pod_name": "api-worker-7b94f9c8-xld4", "node": "ip-10-0-4-12.ec2.internal", "restarts": 14}),
        "entity_vault_lease": ("HashiCorp Vault Lease: db-creds-prod", "VaultLease", {"lease_id": "database/creds/core-api/h78291a", "ttl_remaining": "4m 12s", "renewable": True}),
        "entity_cve_advisory": ("CVE-2024-4367 Security Bulletin", "SecurityAdvisory", {"cve_id": "CVE-2024-4367", "severity": "CRITICAL", "cvss": 9.8, "affected_pkg": "pdfjs-dist"}),
        "entity_kafka_topic": ("Kafka Events Topic: telemetry.raw", "KafkaTopic", {"topic": "telemetry.raw", "partitions": 32, "consumer_lag": 149200, "under_replicated": 0})
    }

    # Add more entities to reach 80
    for j in range(len(entities_dict) + 1, 81):
        entities_dict[f"entity_infra_{j}"] = (
            f"Infrastructure Runtime Entity #{j}",
            "CloudResource",
            {"resource_id": f"res-infra-{j:04d}", "env": "production", "status": "active", "zone": "us-east-1a"}
        )

    # Server to Capabilities mapping
    server_caps_map = {
        "mcp_postgres": (["cap_db_diagnostics", "cap_db_connection_pool", "cap_db_slow_queries"], "entity_pg_cluster_prod"),
        "mcp_mysql": (["cap_db_diagnostics", "cap_db_connection_pool", "cap_db_slow_queries"], "entity_pg_cluster_prod"),
        "mcp_slack": (["cap_incident_alerting"], "entity_slack_incident_room"),
        "mcp_github": (["cap_pr_management", "cap_git_diff"], "entity_github_pr_842"),
        "mcp_docker": (["cap_container_logs", "cap_container_restart"], "entity_docker_container"),
        "mcp_sentry": (["cap_crash_telemetry"], "entity_sentry_issue"),
        "mcp_aws": (["cap_cloud_metrics"], "entity_aws_rds_primary"),
        "mcp_aws_rds": (["cap_cloud_metrics", "cap_db_diagnostics"], "entity_aws_rds_primary"),
        "mcp_k8s": (["cap_k8s_ops", "cap_container_logs"], "entity_k8s_pod"),
        "mcp_vault": (["cap_security_vault"], "entity_vault_lease"),
        "mcp_redis": (["cap_cache_diagnostics"], "entity_redis_cache"),
        "mcp_linear": (["cap_incident_alerting"], "entity_linear_issue"),
        "mcp_datadog": (["cap_apm_tracing"], "entity_datadog_apm"),
        "mcp_splunk": (["cap_log_analytics"], "entity_slack_incident_room"),
        "mcp_kafka": (["cap_streaming_kafka"], "entity_kafka_topic"),
        "mcp_rabbitmq": (["cap_queue_deadletter"], "entity_kafka_topic"),
        "mcp_argocd": (["cap_gitops_argocd"], "entity_github_pr_842"),
        "mcp_circleci": (["cap_ci_pipelines"], "entity_github_pr_842"),
        "mcp_brave": (["cap_cve_search"], "entity_cve_advisory"),
        "mcp_cloudflare": (["cap_dns_edge"], "entity_slack_incident_room"),
        "mcp_stripe": (["cap_billing_audit"], "entity_slack_incident_room"),
    }

    # Now generate all 500 Tools (10 per server)
    tool_counter = 0
    all_entity_keys = list(entities_dict.keys())
    all_cap_keys = list(capabilities_dict.keys())

    for s_idx, (s_id, s_name, s_desc, s_trans, s_ver) in enumerate(servers_raw):
        srv_clean = s_id.replace("mcp_", "")
        domain_name = domain_map.get(s_id, "General Operations")
        default_caps, default_entity = server_caps_map.get(s_id, ([all_cap_keys[s_idx % len(all_cap_keys)]], all_entity_keys[s_idx % len(all_entity_keys)]))
        
        for v_idx, (v_name, v_desc) in enumerate(tool_verbs):
            tool_counter += 1
            
            # Check if this matches one of our exact core tools by server and verb
            matched_core = core_tools_by_server_verb.get((s_id, v_name))

            if matched_core:
                t_id = f"tool_{matched_core[0]}"
                t_name = matched_core[0]
                t_desc = matched_core[1]
                t_cost = matched_core[2]
                primary_cap = matched_core[3]
                primary_entity = matched_core[4]
                initial_pref_weight = 2.4
            else:
                t_id = f"tool_{srv_clean}_{v_name}"
                t_name = f"{srv_clean}_{v_name}"
                t_desc = f"{s_name}: {v_desc} across {domain_name.lower()} workloads."
                t_cost = 380 + (tool_counter * 7) % 220
                primary_cap = default_caps[v_idx % len(default_caps)]
                primary_entity = default_entity
                initial_pref_weight = 1.0 + round((v_idx % 4) * 0.08, 2)

            schema_dict = {
                "type": "object",
                "properties": {
                    "target_identifier": {"type": "string", "description": f"Target entity or resource in {s_name}"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"], "default": "high"},
                    "timeout_seconds": {"type": "integer", "default": 30}
                },
                "required": ["target_identifier"]
            }

            tools_code.append(
                f"    ToolNode(id='{t_id}', name='{t_name}', server_id='{s_id}', description=\"{t_desc}\", parameters_schema={json.dumps(schema_dict)}, estimated_token_cost={t_cost}, invocation_count={10 + tool_counter % 80}, avg_latency_ms={round(45.0 + (tool_counter % 50) * 1.5, 1)}),"
            )
            all_tool_ids.append(t_id)

            # Edge 1: BELONGS_TO (Tool -> MCPServer)
            edges_code.append(
                f"    GraphEdge(source='{t_id}', target='{s_id}', relation='BELONGS_TO', weight=1.0),"
            )

            # Edge 2: PROVIDES (Tool -> Capability)
            edges_code.append(
                f"    GraphEdge(source='{t_id}', target='{primary_cap}', relation='PROVIDES', weight=1.0),"
            )

            # Edge 3: PREFERS (Capability -> Tool, dynamic learning edge)
            edges_code.append(
                f"    GraphEdge(source='{primary_cap}', target='{t_id}', relation='PREFERS', weight={initial_pref_weight}, properties={{'reward_count': {tool_counter % 12}, 'penalty_count': 0}}),"
            )

            # Edge 4: REQUIRES_ENTITY (Tool -> Entity)
            edges_code.append(
                f"    GraphEdge(source='{t_id}', target='{primary_entity}', relation='REQUIRES_ENTITY', weight=1.0),"
            )

            # Edge 5: RESOLVES_ENTITY (for ~40% of tools)
            if tool_counter % 3 == 0:
                secondary_ent = all_entity_keys[(tool_counter * 5) % len(all_entity_keys)]
                edges_code.append(
                    f"    GraphEdge(source='{t_id}', target='{secondary_ent}', relation='RESOLVES_ENTITY', weight=1.0),"
                )

            # Edge 6: CHAINED_TO (Tool -> Tool multi-hop dependency for ~50% of tools)
            if tool_counter > 1 and tool_counter % 2 == 0:
                target_chained_tool = all_tool_ids[tool_counter - 2]
                edges_code.append(
                    f"    GraphEdge(source='{t_id}', target='{target_chained_tool}', relation='CHAINED_TO', weight=1.0, properties={{'chain_reason': 'output_entity_handoff'}}),"
                )

    # Specific core chained workflow edges for canonical scenarios:
    core_chain_pairs = [
        ("tool_pg_check_connection_pool", "tool_slack_post_incident_bulletin"),
        ("tool_pg_check_connection_pool", "tool_github_create_pull_request"),
        ("tool_docker_stream_container_logs", "tool_docker_restart_container"),
        ("tool_sentry_fetch_issue_stacktrace", "tool_github_fetch_commit_diff"),
        ("tool_aws_fetch_rds_metrics", "tool_pg_check_connection_pool")
    ]
    for src, tgt in core_chain_pairs:
        edges_code.append(
            f"    GraphEdge(source='{src}', target='{tgt}', relation='CHAINED_TO', weight=1.5, properties={{'canonical_path': True}}),"
        )

    # Capabilities code
    caps_code = []
    for c_id, (c_name, c_dom, c_keys) in capabilities_dict.items():
        caps_code.append(
            f"    CapabilityNode(id='{c_id}', name='{c_name}', domain='{c_dom}', keywords={c_keys}),"
        )

    # Entities code
    ents_code = []
    for e_id, (e_name, e_type, e_props) in entities_dict.items():
        ents_code.append(
            f"    EntityNode(id='{e_id}', name='{e_name}', entity_type='{e_type}', properties={repr(e_props)}),"
        )

    # Write out Python file
    content = f'''"""
Lucen Seed Dataset - Scaled Enterprise MCP Ecosystem, Tools, and Context Entities
50 MCP Servers | 500 Enterprise Tools | 100 Capabilities | 80 Pre-Bound Entities | 2,500+ GraphBLAS Edges
"""
from typing import Dict, List, Any
from backend.models import MCPServerNode, ToolNode, CapabilityNode, EntityNode, GraphEdge

MCP_SERVERS: List[MCPServerNode] = [
{chr(10).join(servers_code)}
]

CAPABILITIES: List[CapabilityNode] = [
{chr(10).join(caps_code)}
]

ENTITIES: List[EntityNode] = [
{chr(10).join(ents_code)}
]

TOOLS: List[ToolNode] = [
{chr(10).join(tools_code)}
]

EDGES: List[GraphEdge] = [
{chr(10).join(edges_code)}
]
'''
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated {out_file} successfully:")
    print(f"  Servers:      {len(servers_raw)}")
    print(f"  Tools:        {len(tools_code)}")
    print(f"  Capabilities: {len(caps_code)}")
    print(f"  Entities:     {len(ents_code)}")
    print(f"  Edges:        {len(edges_code)}")

if __name__ == "__main__":
    build()
