import os
import json

def generate_catalog():
    # 50 Enterprise MCP Servers
    servers_raw = [
        # Databases (10)
        ("mcp_postgres", "PostgreSQL Inspector", "Live inspection, connection pool health, vacuum metrics, and slow query EXPLAIN analysis", "stdio", "3.2.0"),
        ("mcp_mysql", "MySQL Enterprise", "InnoDB buffer pool monitoring, replication lag metrics, deadlock detection, and slow query log", "stdio", "2.1.4"),
        ("mcp_redis", "Redis Cluster Engine", "Key eviction monitoring, memory fragmentation analysis, pub/sub throughput, and cache warmup", "stdio", "4.0.1"),
        ("mcp_clickhouse", "ClickHouse OLAP", "Distributed table query performance, merge tree part inspection, and column compression stats", "stdio", "1.5.0"),
        ("mcp_snowflake", "Snowflake Data Cloud", "Warehouse credit consumption, virtual cluster autoscaling, query acceleration, and role grants", "sse", "2.0.8"),
        ("mcp_bigquery", "Google BigQuery", "Slot allocation monitoring, partition pruning validation, job execution graphs, and dry-run cost estimation", "sse", "1.9.2"),
        ("mcp_mongodb", "MongoDB Atlas", "Replica set oplog lag, wiredTiger cache pressure, slow collection query profiling, and index sizing", "stdio", "2.3.1"),
        ("mcp_elasticsearch", "Elasticsearch Core", "Cluster shard allocation, JVM garbage collection pauses, search thread pool queue, and index lifecycle", "stdio", "3.0.0"),
        ("mcp_kafka", "Apache Kafka Streaming", "Consumer group lag inspection, partition leader rebalancing, broker under-replicated partitions, and topic offsets", "stdio", "2.4.0"),
        ("mcp_rabbitmq", "RabbitMQ Broker", "Queue depth monitoring, consumer acknowledgment rates, unacked message deadlettering, and channel churn", "stdio", "1.8.0"),

        # Cloud & Compute (8)
        ("mcp_aws", "AWS Cloud Ops", "EC2 instance status, CloudWatch composite alarms, VPC flow logs, and IAM credential rotation", "stdio", "2.6.0"),
        ("mcp_aws_rds", "AWS RDS Engine", "Multi-AZ failover triggering, Aurora read replica auto-scaling, IOPS burst balance, and storage autoscaling", "stdio", "2.2.0"),
        ("mcp_aws_lambda", "AWS Lambda Runtime", "Cold start telemetry, provisioned concurrency metrics, dead-letter queue inspection, and layer updates", "stdio", "1.7.0"),
        ("mcp_aws_ecs", "AWS ECS & Fargate", "Service deployment draining, task memory limit alerts, rolling updates, and container definitions", "stdio", "2.1.0"),
        ("mcp_k8s", "Kubernetes Cluster Admin", "Pod crashloop detection, horizontal pod autoscaler status, node drain, ingress routing, and secret mounts", "stdio", "3.4.0"),
        ("mcp_docker", "Docker Container Runtime", "Container stderr streaming, memory OOM kill diagnosis, zero-downtime rolling restart, and image layer prune", "stdio", "2.0.2"),
        ("mcp_terraform", "Terraform Cloud Infra", "Workspace speculative plan generation, drift detection, state lock release, and policy cost estimation", "sse", "1.4.0"),
        ("mcp_cloudflare", "Cloudflare Edge & DNS", "DNS record propagation, WAF managed rule toggles, rate limit rule configuration, and cache purge", "sse", "2.0.1"),

        # Observability & APM (8)
        ("mcp_datadog", "Datadog Telemetry", "APM trace waterfall inspection, synthetic monitor outages, host agent health, and anomaly detector queries", "stdio", "2.5.0"),
        ("mcp_splunk", "Splunk Log Analytics", "Enterprise SPL log search, index rate spikes, forwarder disconnects, and saved alert bulletin dispatch", "stdio", "1.9.0"),
        ("mcp_sentry", "Sentry Crash Telemetry", "Real-time unhandled exception stacktraces, culprit commit identification, release health, and user impact", "stdio", "2.1.2"),
        ("mcp_grafana", "Grafana Dashboard Engine", "PromQL dashboard snapshot generation, panel alert state verification, and data source query latency", "sse", "2.2.0"),
        ("mcp_prometheus", "Prometheus Metric Scraper", "Vector instant queries, range queries across scrape targets, recording rule status, and alertmanager rules", "stdio", "2.8.0"),
        ("mcp_pagerduty", "PagerDuty Incident Ops", "On-call schedule resolution, high-urgency incident escalation, responder engagement, and service status", "sse", "2.0.0"),
        ("mcp_newrelic", "New Relic APM", "Golden signal latency profiling, database transaction breakdown, and JVM thread deadlock analysis", "stdio", "1.6.0"),
        ("mcp_honeycomb", "Honeycomb Tracing", "High-cardinality bubble-up analysis, span attribute filtering, and distributed service latency traces", "stdio", "1.3.0"),

        # Development & Source Control (8)
        ("mcp_github", "GitHub Repo Manager", "Pull Request hotfix creation, branch protection enforcement, commit blame, and reviewer assignment", "stdio", "3.3.0"),
        ("mcp_gitlab", "GitLab CI/CD Engine", "Pipeline job retry, merge request status, environment deployment rollbacks, and runner health", "stdio", "2.0.0"),
        ("mcp_linear", "Linear Issue Tracker", "Urgent incident ticket triage, GitHub PR linkage, SLA countdown, and engineering ownership assignment", "sse", "2.2.0"),
        ("mcp_jira", "Jira Enterprise", "Production blocker creation, sprint workflow transitions, priority escalation, and audit logging", "sse", "1.9.5"),
        ("mcp_argocd", "ArgoCD GitOps Engine", "Application sync status, out-of-sync diff visualization, automated rollbacks, and manifest refresh", "stdio", "2.4.0"),
        ("mcp_circleci", "CircleCI Workflow Automation", "Pipeline step parallelism, failed step log inspection, cache clear, and rerun from failed step", "stdio", "1.5.0"),
        ("mcp_snyk", "Snyk Security Inspector", "Vulnerable open-source dependency scanning, container base image CVE check, and fix PR drafting", "stdio", "1.8.0"),
        ("mcp_sonarqube", "SonarQube Code Analyzer", "Quality gate status, code smell severity breakdown, test coverage delta, and security hotspot triage", "stdio", "1.7.0"),

        # Networking & Security (6)
        ("mcp_vault", "HashiCorp Vault", "Dynamic database credential leases, KV v2 secret retrieval, transit secret encryption, and approle token renew", "stdio", "2.2.0"),
        ("mcp_aws_iam", "AWS IAM Auth Inspector", "Unused privilege escalation audits, policy simulator validation, role assumption, and MFA enforcement", "stdio", "1.9.0"),
        ("mcp_okta", "Okta Identity Manager", "Employee session suspension, MFA token reset, SAML application assignment, and directory sync", "sse", "2.0.0"),
        ("mcp_fastly", "Fastly Edge CDN", "Surrogate key cache purging, VCL snippet compilation, edge rate limit inspection, and origin shielding", "stdio", "1.4.0"),
        ("mcp_wireguard", "WireGuard Mesh VPN", "Peer handshake status, client public key verification, routing table inspection, and tunnel restart", "stdio", "1.2.0"),
        ("mcp_nginx", "NGINX Ingress Controller", "Upstream server health check status, TLS certificate expiry verification, and rate limit bucket metrics", "stdio", "2.0.0"),

        # Comms & Team Collaboration (5)
        ("mcp_slack", "Slack Enterprise", "Incident war room message broadcast, thread updates, user paging, and incident channel creation", "sse", "2.5.0"),
        ("mcp_discord", "Discord DevOps", "Engineering operations webhook alerts, voice stage paging, and automated changelog publishing", "stdio", "1.5.0"),
        ("mcp_notion", "Notion Engineering Hub", "Incident postmortem doc generation, architecture decision records (ADR) update, and runbook retrieval", "sse", "2.1.0"),
        ("mcp_confluence", "Confluence Wiki", "Postmortem space creation, system runbook indexing, emergency operational procedure search", "sse", "1.8.0"),
        ("mcp_oncall", "OpsGenie On-Call Router", "Rotation schedule verification, override generation, heart-beat monitoring, and responder notification", "sse", "1.6.0"),

        # Payments & Business APIs (3)
        ("mcp_stripe", "Stripe Financial Engine", "Charge dispute investigation, customer subscription status, webhook delivery retry, and refund authorization", "sse", "2.4.0"),
        ("mcp_twilio", "Twilio SMS Notification", "Urgent executive SMS paging, delivery receipt status, phone number lookup, and voice call dispatch", "stdio", "1.3.0"),
        ("mcp_sendgrid", "SendGrid Delivery", "Transactional email delivery logs, bounce rate inspection, domain authentication verification, and suppression list", "stdio", "1.5.0"),

        # AI & Search (2)
        ("mcp_brave", "Brave Search Engine", "External technical search, official documentation retrieval, CVE vulnerability lookups, and library changelogs", "sse", "2.0.0"),
        ("mcp_perplexity", "Perplexity Deep Research", "Multi-source research synthesis, academic paper references, and root cause postmortem analysis across public outages", "sse", "1.8.0")
    ]

    print(f"Total Servers Configured: {len(servers_raw)}")

    # 10 tools per server template
    tool_verbs = [
        ("inspect_health", "Queries real-time health, uptime, and cluster consensus metrics"),
        ("fetch_metrics", "Retrieves telemetry time-series, throughput, and error rate percentages"),
        ("check_connection_pool", "Inspects active connections, idle timeouts, and client queue depth"),
        ("stream_logs", "Streams recent stderr and stdout log records with severity filter"),
        ("trigger_restart", "Initiates graceful rolling restart without service interruption"),
        ("execute_rebalance", "Rebalances cluster nodes, shards, or partitions to alleviate hotspots"),
        ("drain_traffic", "Safely drains active client traffic prior to maintenance window"),
        ("verify_configuration", "Validates runtime config parameters against baseline compliance"),
        ("dispatch_alert", "Dispatches high-urgency notifications to designated operational channels"),
        ("generate_diagnostic_report", "Compiles comprehensive JSON diagnostic snapshot for root cause analysis")
    ]

    return servers_raw, tool_verbs

if __name__ == "__main__":
    generate_catalog()
