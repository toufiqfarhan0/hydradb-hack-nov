# Fidelity Differential: Graph Reachability vs Baselines

This document analyzes why traditional context selection mechanisms (Naive Preloading, Vector Embeddings, BM25, and Flat Key-Value lookups) fail on enterprise operational topologies, and how Lucen achieves 93.3% tool recall and 100% runtime entity binding.

---

## 1. Architectural Comparison Matrix

| Context Selection Strategy | Disambiguates Environment (Prod vs Staging) | Multi-Hop Dependency Chains | Turn-0 Zero-Shot Success | Token Footprint (500 Tools) | Lost Update Resilience |
|---|---|---|---|---|---|
| **Naive Full Preload** | No (Relies on model prompt inference) | No (All tools dumped into context) | 0.0% (0/15) | 272,607 tokens | N/A |
| **BM25 Keyword Search (Top-4)** | No (Matches lexical tokens only) | No (Single-hop keyword matching) | 0.0% (0/15) | 2,273 tokens | N/A |
| **Hardened BM25 (k=16)** | No | No | 46.7% (7/15) | 7,653 tokens | N/A |
| **Flat Keyed Map `{(svc, env): entity}`** | Partial (Requires exact composite key) | No (Cannot traverse service -> cluster -> replica) | 46.7% (7/15) | ~2,500 tokens | No (App-level locks required) |
| **Lucen (HydraDB GraphBLAS)** | **Yes** (Graph topology binds environment) | **Yes** (Incident -> Service -> Cluster -> Replicas) | **86.7% (13/15)** | **1,214 tokens** | **Yes (In-engine atomic delta updates)** |

---

## 2. The Multi-Hop Disambiguation Problem

A naive 1:1 `{tool: entity}` map fails in any realistic infrastructure topology because a tool does not belong to a single entity. 

Consider an incident prompt:
```
"Alert: auth-service database connection pool exhausted in production."
```

In an enterprise environment:
- There is a `pg_check_connection_pool` tool.
- There are multiple database clusters:
  - `pg-cluster-prod.internal:5432` (Production Master)
  - `pg-cluster-staging.internal:5432` (Staging Master)
  - `pg-cluster-analytics.internal:5432` (Data Warehouse)
  - `pg-cluster-prod-ro-01.internal:5432` (Read Replica)

### Why Vector Search & BM25 Fail
Vector embeddings compare semantic cosine similarity between the prompt and tool descriptions:
- Query: `"auth-service database connection pool exhausted in production"`
- Vector top matches: `pg_check_connection_pool`, `datadog_query_metrics`, `sentry_get_issue`.
- **The Blind Spot**: Vector retrieval retrieves the schema of `pg_check_connection_pool`, but the schema requires arguments: `host: string`, `database: string`.
- Because vector databases index static documentation text, they have zero access to the live runtime infrastructure topology. The agent receives empty parameter templates and must spend 2 to 3 exploratory turns asking: *"What is the hostname of the production database for auth-service?"*

### Why Flat Key-Value Maps Break
Even if a developer introduces a composite dictionary like `{(service, env): database_host}`, this breaks the moment traversal requires multi-hop discovery:
1. `auth-service` does not talk directly to a standalone database; it connects via a PgBouncer connection pooler container.
2. The incident involves a replica lag failover where the write pool has shifted to an alternate host.
3. Resolving the true failure requires traversing:
   `Incident(alert) -> Service(auth-service) -> Cluster(pg-cluster-prod) -> Pooler(pgbouncer-prod-01) -> Primary(pg-cluster-prod-01)`.

A flat map requires hardcoding every permutation in advance. A graph represents this naturally as nodes and edges.

---

## 3. How Lucen Traverses the Topology

In Lucen, when an incident arrives, OpenCypher traverses the topological graph:

```cypher
MATCH (inc:Incident {id: $incident_id})-[:AFFECTS]->(svc:Service)
MATCH (svc)-[:CONNECTS_TO]->(c:Cluster {environment: 'production'})
MATCH (c)-[:HAS_NODE]->(db:DatabaseNode)
MATCH (t:Tool)-[:MANAGES]->(db)
OPTIONAL MATCH (agent:Agent)-[p:PREFERS]->(t)
RETURN t.name, t.schema, db.hostname, db.port, coalesce(p.weight, 1.0) AS weight
ORDER BY weight DESC
LIMIT 4;
```

This single query:
1. Filters out staging and analytics databases deterministically.
2. Identifies the primary production database host (`pg-cluster-prod.internal:5432`).
3. Pre-binds the hostname and credentials directly into the tool context envelope.
4. Ranks the reachable tools using dynamically reinforced weights learned from past incident resolutions.

---

## 4. Empirical Evaluation on Held-Out Scenarios

Across 15 held-out enterprise incident scenarios:
- **Tool Recall**: Lucen achieved **93.3%** recall of the exact tools needed to diagnose and resolve the incident.
- **Entity Pre-Binding Accuracy**: **100.0%**. Every tool passed to the LLM was populated with pre-bound runtime targets (hostname, port, database name, channel ID).
- **Turn-0 Zero-Shot Execution**: **86.7% (13/15)** of incidents were successfully resolved on the very first LLM execution turn without requiring human intervention or exploratory turns.

To inspect the held-out evaluation test harness:
```bash
python eval/benchmark_eval.py
```
