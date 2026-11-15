"""
50 Real-World Enterprise Operational Scenarios
Dataset with Train / Held-Out Test Split for Continual Learning Benchmarking.
Contains 35 Training Tasks and 15 Held-Out Test Tasks.
"""
from typing import List, Dict, Any

TASKS_DATASET: List[Dict[str, Any]] = [
    # --- TRAINING TASKS (1 to 35) ---
    {
        "id": "task_01",
        "split": "train",
        "query": "Production PostgreSQL database is exhausting connection pool and throwing 500s. Inspect pool and broadcast alert to Slack war room.",
        "expected_tools": ["tool_pg_check_connection_pool", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_pg_cluster_prod", "entity_slack_incident_room"],
        "category": "database_incident"
    },
    {
        "id": "task_02",
        "split": "train",
        "query": "Core API container crashed with OOMKilled exit code 137. Stream stderr logs and trigger graceful container restart.",
        "expected_tools": ["tool_docker_stream_container_logs", "tool_docker_restart_container"],
        "expected_entities": ["entity_docker_container"],
        "category": "container_lifecycle"
    },
    {
        "id": "task_03",
        "split": "train",
        "query": "Sentry reported unhandled DeadlockDetected exception in billing worker. Fetch stacktrace and create urgent hotfix PR on GitHub.",
        "expected_tools": ["tool_sentry_fetch_issue_stacktrace", "tool_github_create_pull_request"],
        "expected_entities": ["entity_sentry_issue", "entity_github_pr_842"],
        "category": "incident_remediation"
    },
    {
        "id": "task_04",
        "split": "train",
        "query": "AWS Aurora primary replica IOPS burst balance dropping below 10%. Inspect RDS metrics and check connection pool status.",
        "expected_tools": ["tool_aws_fetch_rds_metrics", "tool_pg_check_connection_pool"],
        "expected_entities": ["entity_aws_rds_primary", "entity_pg_cluster_prod"],
        "category": "cloud_infra"
    },
    {
        "id": "task_05",
        "split": "train",
        "query": "Redis session cache experiencing key eviction spike and latency degradation. Check eviction metrics and inspect memory.",
        "expected_tools": ["tool_redis_inspect_eviction_spikes", "tool_redis_fetch_metrics"],
        "expected_entities": ["entity_redis_cache"],
        "category": "cache_performance"
    },
    {
        "id": "task_06",
        "split": "train",
        "query": "Kubernetes worker pod stuck in CrashLoopBackOff on production node. Describe crashing pod and check container stderr logs.",
        "expected_tools": ["tool_k8s_describe_crashing_pod", "tool_docker_stream_container_logs"],
        "expected_entities": ["entity_k8s_pod", "entity_docker_container"],
        "category": "k8s_lifecycle"
    },
    {
        "id": "task_07",
        "split": "train",
        "query": "HashiCorp Vault dynamic Postgres credential lease expiring in 4 minutes. Renew database lease and post status to Slack.",
        "expected_tools": ["tool_vault_renew_database_lease", "tool_slack_update_incident_status"],
        "expected_entities": ["entity_vault_lease", "entity_slack_incident_room"],
        "category": "security_ops"
    },
    {
        "id": "task_08",
        "split": "train",
        "query": "Linear incident ticket INC-492 created for API degradation. Inspect Datadog APM waterfall traces and link GitHub PR.",
        "expected_tools": ["tool_datadog_query_apm_traces", "tool_linear_create_incident_issue"],
        "expected_entities": ["entity_datadog_apm", "entity_linear_issue"],
        "category": "incident_tracking"
    },
    {
        "id": "task_09",
        "split": "train",
        "query": "Kafka raw telemetry topic consumer lag spiked to 150k messages. Check consumer partition lag and verify broker health.",
        "expected_tools": ["tool_kafka_fetch_metrics", "tool_kafka_inspect_health"],
        "expected_entities": ["entity_kafka_topic"],
        "category": "streaming_ops"
    },
    {
        "id": "task_10",
        "split": "train",
        "query": "CVE security advisory reported on production frontend dependency. Search CVE bulletins and draft security fix PR on GitHub.",
        "expected_tools": ["tool_brave_search_cve_advisories", "tool_github_create_pull_request"],
        "expected_entities": ["entity_cve_advisory", "entity_github_pr_842"],
        "category": "security_vulnerability"
    },
    {
        "id": "task_11",
        "split": "train",
        "query": "Slow queries locking customer tables on PostgreSQL. Execute EXPLAIN query analysis and check table bloat.",
        "expected_tools": ["tool_pg_explain_slow_query", "tool_pg_inspect_table_bloat"],
        "expected_entities": ["entity_pg_cluster_prod"],
        "category": "database_diagnostics"
    },
    {
        "id": "task_12",
        "split": "train",
        "query": "Idle in transaction sessions blocking write locks on primary database. Terminate idle sessions and broadcast status to Slack.",
        "expected_tools": ["tool_pg_kill_idle_in_transaction", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_pg_cluster_prod", "entity_slack_incident_room"],
        "category": "database_incident"
    },
    {
        "id": "task_13",
        "split": "train",
        "query": "Recent deployment caused regression in checkout flow. Fetch git commit diff and create Linear incident ticket.",
        "expected_tools": ["tool_github_fetch_commit_diff", "tool_linear_create_incident_issue"],
        "expected_entities": ["entity_github_pr_842", "entity_linear_issue"],
        "category": "incident_tracking"
    },
    {
        "id": "task_14",
        "split": "train",
        "query": "Container memory consumption exceeding 95% threshold. Drain traffic from task and trigger container restart.",
        "expected_tools": ["tool_docker_drain_traffic", "tool_docker_restart_container"],
        "expected_entities": ["entity_docker_container"],
        "category": "container_lifecycle"
    },
    {
        "id": "task_15",
        "split": "train",
        "query": "Failing Kubernetes node causing pod evictions. Drain node safely and notify Slack critical ops channel.",
        "expected_tools": ["tool_k8s_drain_failing_node", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_k8s_pod", "entity_slack_incident_room"],
        "category": "k8s_lifecycle"
    },
    {
        "id": "task_16",
        "split": "train",
        "query": "MySQL database experiencing deadlocks in InnoDB buffer pool. Check connection pool and inspect query logs.",
        "expected_tools": ["tool_mysql_check_connection_pool", "tool_mysql_stream_logs"],
        "expected_entities": ["entity_pg_cluster_prod"],
        "category": "database_diagnostics"
    },
    {
        "id": "task_17",
        "split": "train",
        "query": "CloudWatch reporting high CPU utilization on primary RDS database. Fetch RDS metrics and check slow query EXPLAIN.",
        "expected_tools": ["tool_aws_fetch_rds_metrics", "tool_pg_explain_slow_query"],
        "expected_entities": ["entity_aws_rds_primary", "entity_pg_cluster_prod"],
        "category": "cloud_infra"
    },
    {
        "id": "task_18",
        "split": "train",
        "query": "Datadog APM alert for 5xx error rate spike on core API. Query APM traces and fetch Sentry crash stacktrace.",
        "expected_tools": ["tool_datadog_query_apm_traces", "tool_sentry_fetch_issue_stacktrace"],
        "expected_entities": ["entity_datadog_apm", "entity_sentry_issue"],
        "category": "observability"
    },
    {
        "id": "task_19",
        "split": "train",
        "query": "Urgent incident ticket triage in Linear. Update incident status and post bulletin to Slack war room.",
        "expected_tools": ["tool_slack_update_incident_status", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_slack_incident_room"],
        "category": "incident_response"
    },
    {
        "id": "task_20",
        "split": "train",
        "query": "Redis cluster memory fragmentation reaching critical threshold. Trigger cache rebalance and check health.",
        "expected_tools": ["tool_redis_execute_rebalance", "tool_redis_inspect_health"],
        "expected_entities": ["entity_redis_cache"],
        "category": "cache_performance"
    },
    {
        "id": "task_21",
        "split": "train",
        "query": "Stripe webhook dispute received for charge failure. Verify transaction logs and dispatch alert to Slack.",
        "expected_tools": ["tool_stripe_stream_logs", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_slack_incident_room"],
        "category": "business_ops"
    },
    {
        "id": "task_22",
        "split": "train",
        "query": "Cloudflare edge WAF rules detecting suspicious DDoS pattern. Inspect edge metrics and update rate limit rules.",
        "expected_tools": ["tool_cloudflare_fetch_metrics", "tool_cloudflare_verify_configuration"],
        "expected_entities": ["entity_slack_incident_room"],
        "category": "edge_networking"
    },
    {
        "id": "task_23",
        "split": "train",
        "query": "Splunk log aggregator reporting spike in fatal auth exceptions. Stream Splunk logs and search CVE advisories.",
        "expected_tools": ["tool_splunk_stream_logs", "tool_brave_search_cve_advisories"],
        "expected_entities": ["entity_cve_advisory"],
        "category": "log_analytics"
    },
    {
        "id": "task_24",
        "split": "train",
        "query": "RabbitMQ dead-letter queue piling up with unacknowledged messages. Inspect queue depth and check connection pool.",
        "expected_tools": ["tool_rabbitmq_fetch_metrics", "tool_rabbitmq_check_connection_pool"],
        "expected_entities": ["entity_kafka_topic"],
        "category": "messaging"
    },
    {
        "id": "task_25",
        "split": "train",
        "query": "Terraform Cloud infrastructure drift detected in production VPC. Generate speculative plan and check AWS RDS status.",
        "expected_tools": ["tool_terraform_verify_configuration", "tool_aws_fetch_rds_metrics"],
        "expected_entities": ["entity_aws_rds_primary"],
        "category": "iac"
    },
    {
        "id": "task_26",
        "split": "train",
        "query": "ArgoCD gitops deployment out of sync with main branch. Inspect manifest sync status and check GitHub PR.",
        "expected_tools": ["tool_argocd_verify_configuration", "tool_github_create_pull_request"],
        "expected_entities": ["entity_github_pr_842"],
        "category": "gitops"
    },
    {
        "id": "task_27",
        "split": "train",
        "query": "Grafana panel alert firing for database read replica latency. Inspect Grafana dashboard snapshot and RDS metrics.",
        "expected_tools": ["tool_grafana_fetch_metrics", "tool_aws_fetch_rds_metrics"],
        "expected_entities": ["entity_aws_rds_primary"],
        "category": "observability"
    },
    {
        "id": "task_28",
        "split": "train",
        "query": "Prometheus scrape target failing for core API worker. Query instant vector scrape metrics and check pod status.",
        "expected_tools": ["tool_prometheus_fetch_metrics", "tool_k8s_describe_crashing_pod"],
        "expected_entities": ["entity_k8s_pod"],
        "category": "observability"
    },
    {
        "id": "task_29",
        "split": "train",
        "query": "PagerDuty on-call escalation for database outage. Fetch on-call schedule and post incident bulletin to Slack.",
        "expected_tools": ["tool_pagerduty_dispatch_alert", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_slack_incident_room"],
        "category": "incident_response"
    },
    {
        "id": "task_30",
        "split": "train",
        "query": "Elasticsearch search thread pool queue rejected queries. Inspect cluster shard health and fetch node metrics.",
        "expected_tools": ["tool_elasticsearch_inspect_health", "tool_elasticsearch_fetch_metrics"],
        "expected_entities": ["entity_redis_cache"],
        "category": "search_indexing"
    },
    {
        "id": "task_31",
        "split": "train",
        "query": "GitHub pull request review failed automated security scan. Fetch commit diff and search CVE vulnerability details.",
        "expected_tools": ["tool_github_fetch_commit_diff", "tool_brave_search_cve_advisories"],
        "expected_entities": ["entity_github_pr_842", "entity_cve_advisory"],
        "category": "security_review"
    },
    {
        "id": "task_32",
        "split": "train",
        "query": "High connection churn on PgBouncer proxy. Check connection pool metrics and inspect table bloat.",
        "expected_tools": ["tool_pg_check_connection_pool", "tool_pg_inspect_table_bloat"],
        "expected_entities": ["entity_pg_cluster_prod"],
        "category": "database_diagnostics"
    },
    {
        "id": "task_33",
        "split": "train",
        "query": "Sentry release telemetry indicating 40% crash rate on v2.14. Fetch crash stacktrace and stream container stderr.",
        "expected_tools": ["tool_sentry_fetch_issue_stacktrace", "tool_docker_stream_container_logs"],
        "expected_entities": ["entity_sentry_issue", "entity_docker_container"],
        "category": "crash_diagnostics"
    },
    {
        "id": "task_34",
        "split": "train",
        "query": "Kubernetes node memory starvation causing evictions. Describe crashing pod and drain failing node.",
        "expected_tools": ["tool_k8s_describe_crashing_pod", "tool_k8s_drain_failing_node"],
        "expected_entities": ["entity_k8s_pod"],
        "category": "k8s_lifecycle"
    },
    {
        "id": "task_35",
        "split": "train",
        "query": "HashiCorp Vault token renewal failure blocking worker boot. Renew database credentials lease and check logs.",
        "expected_tools": ["tool_vault_renew_database_lease", "tool_vault_stream_logs"],
        "expected_entities": ["entity_vault_lease"],
        "category": "security_ops"
    },

    # --- HELD-OUT TEST TASKS (36 to 50) ---
    # These tasks are NEVER used to update edge weights during training.
    # Evaluated at every checkpoint to measure true generalization.
    {
        "id": "task_36",
        "split": "test",
        "query": "Major database connection pool exhaustion on primary cluster during peak traffic. Check pool stats and broadcast to Slack war room.",
        "expected_tools": ["tool_pg_check_connection_pool", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_pg_cluster_prod", "entity_slack_incident_room"],
        "category": "held_out_database"
    },
    {
        "id": "task_37",
        "split": "test",
        "query": "Production API worker exited with SIGKILL 137. Stream container stderr logs and restart Docker container.",
        "expected_tools": ["tool_docker_stream_container_logs", "tool_docker_restart_container"],
        "expected_entities": ["entity_docker_container"],
        "category": "held_out_container"
    },
    {
        "id": "task_38",
        "split": "test",
        "query": "Critical unhandled exception detected in payment microservice. Retrieve Sentry stacktrace and open emergency GitHub hotfix PR.",
        "expected_tools": ["tool_sentry_fetch_issue_stacktrace", "tool_github_create_pull_request"],
        "expected_entities": ["entity_sentry_issue", "entity_github_pr_842"],
        "category": "held_out_remediation"
    },
    {
        "id": "task_39",
        "split": "test",
        "query": "Aurora RDS read replica lagging behind primary. Check AWS RDS metrics and inspect PostgreSQL connection pool.",
        "expected_tools": ["tool_aws_fetch_rds_metrics", "tool_pg_check_connection_pool"],
        "expected_entities": ["entity_aws_rds_primary", "entity_pg_cluster_prod"],
        "category": "held_out_cloud"
    },
    {
        "id": "task_40",
        "split": "test",
        "query": "Redis cache eviction rate spiking above threshold. Inspect key evictions and check Redis cluster health.",
        "expected_tools": ["tool_redis_inspect_eviction_spikes", "tool_redis_inspect_health"],
        "expected_entities": ["entity_redis_cache"],
        "category": "held_out_cache"
    },
    {
        "id": "task_41",
        "split": "test",
        "query": "Kubernetes pod crashing repeatedly with OutOfMemory error. Describe pod and drain worker node.",
        "expected_tools": ["tool_k8s_describe_crashing_pod", "tool_k8s_drain_failing_node"],
        "expected_entities": ["entity_k8s_pod"],
        "category": "held_out_k8s"
    },
    {
        "id": "task_42",
        "split": "test",
        "query": "Expiring database credentials lease in HashiCorp Vault. Renew dynamic lease and notify Slack incident room.",
        "expected_tools": ["tool_vault_renew_database_lease", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_vault_lease", "entity_slack_incident_room"],
        "category": "held_out_security"
    },
    {
        "id": "task_43",
        "split": "test",
        "query": "Degraded P99 response time on core API service. Query Datadog APM traces and create Linear incident ticket.",
        "expected_tools": ["tool_datadog_query_apm_traces", "tool_linear_create_incident_issue"],
        "expected_entities": ["entity_datadog_apm", "entity_linear_issue"],
        "category": "held_out_apm"
    },
    {
        "id": "task_44",
        "split": "test",
        "query": "Severe partition lag on Kafka event stream. Inspect Kafka consumer lag and check broker health status.",
        "expected_tools": ["tool_kafka_fetch_metrics", "tool_kafka_inspect_health"],
        "expected_entities": ["entity_kafka_topic"],
        "category": "held_out_streaming"
    },
    {
        "id": "task_45",
        "split": "test",
        "query": "Zero-day vulnerability discovered in node package. Search CVE advisory bulletin and create GitHub hotfix PR.",
        "expected_tools": ["tool_brave_search_cve_advisories", "tool_github_create_pull_request"],
        "expected_entities": ["entity_cve_advisory", "entity_github_pr_842"],
        "category": "held_out_cve"
    },
    {
        "id": "task_46",
        "split": "test",
        "query": "Database queries taking over 10 seconds to execute. Run EXPLAIN query plan analysis and check table bloat on Postgres.",
        "expected_tools": ["tool_pg_explain_slow_query", "tool_pg_inspect_table_bloat"],
        "expected_entities": ["entity_pg_cluster_prod"],
        "category": "held_out_database"
    },
    {
        "id": "task_47",
        "split": "test",
        "query": "Idle database transactions holding lock table. Terminate idle sessions and notify Slack critical operations.",
        "expected_tools": ["tool_pg_kill_idle_in_transaction", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_pg_cluster_prod", "entity_slack_incident_room"],
        "category": "held_out_database"
    },
    {
        "id": "task_48",
        "split": "test",
        "query": "Production regression detected after merge. Inspect git commit diff and open hotfix PR on GitHub.",
        "expected_tools": ["tool_github_fetch_commit_diff", "tool_github_create_pull_request"],
        "expected_entities": ["entity_github_pr_842"],
        "category": "held_out_git"
    },
    {
        "id": "task_49",
        "split": "test",
        "query": "Container resource limits exceeded on gateway. Drain traffic safely and restart container.",
        "expected_tools": ["tool_docker_drain_traffic", "tool_docker_restart_container"],
        "expected_entities": ["entity_docker_container"],
        "category": "held_out_container"
    },
    {
        "id": "task_50",
        "split": "test",
        "query": "Failing Kubernetes worker node impacting multiple pods. Drain node and broadcast incident bulletin to Slack.",
        "expected_tools": ["tool_k8s_drain_failing_node", "tool_slack_post_incident_bulletin"],
        "expected_entities": ["entity_k8s_pod", "entity_slack_incident_room"],
        "category": "held_out_k8s"
    }
]
