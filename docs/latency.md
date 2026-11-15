# Latency Profile & Micro-Benchmark Report

This document details the latency profile, micro-benchmarks, and scaling behavior of Lucen's context resolution engine across hardware and storage backends.

---

## 1. Executive Summary

| Layer | Implementation | Operation | Mean Latency | p95 Latency | p99 Latency | Complexity |
|---|---|---|---|---|---|---|
| **Memory CSR** | SuiteSparse GraphBLAS / SciPy CSR | 2-Hop Transitive Reachability | **0.21 ms** | 0.28 ms | 0.35 ms | `O(nnz)` |
| **In-Memory SQL** | SQLite 3.45 Recursive CTE | 2-Hop CTE Query | **0.016 ms** | 0.024 ms | 0.041 ms | `O(E * V)` |
| **Flat Hash Map** | Python 3.11 In-Memory Dict | 1:1 Direct Key Lookup | **0.001 ms** | 0.002 ms | 0.004 ms | `O(1)` |
| **HydraDB Engine** | HydraDB HTTP OpenCypher Gateway | Full Cypher Pattern Match & Filter | **6.42 ms** | 8.15 ms | 11.20 ms | `O(E_subgraph)` |
| **Naive LLM Turn** | 272k Token System Prompt Serialization | Time-To-First-Token (TTFT) | **1,840 ms** | 2,120 ms | 2,450 ms | `O(N_tokens)` |
| **Lucen LLM Turn** | 1.2k Token System Prompt (Filtered) | Time-To-First-Token (TTFT) | **115 ms** | 132 ms | 155 ms | `O(N_pruned)` |

Reproduce these numbers locally via:
```bash
python lucen.py verify
python lucen.py ablation
```

---

## 2. Why Not Just Use Python Dict or SQLite?

A common question in graph database evaluations is why an engineering team shouldn't simply use an in-memory hash map (`dict`) or embedded SQLite database.

Our benchmark (`python lucen.py ablation`) compares all three under both read traversal and concurrent write conditions:

### A. Read Path (Single-Threaded Lookups)
- **Python Dict (`0.001 ms`)**: Unbeatable on flat 1-hop lookups (`tool_name -> metadata`). However, it cannot perform relational multi-hop path reachability (`Incident -> Service -> Database Cluster -> Tool`) without writing custom recursive application logic that reimplements graph traversal in memory.
- **SQLite CTE (`0.016 ms`)**: Performs well on small in-memory tables. However, multi-hop queries require complex recursive CTEs or multi-table JOINs across entity tables, relation tables, and tool schema tables.
- **Embedded CSR GraphBLAS (`0.21 ms`)**: Lowered to sparse matrix-vector multiplication (`semiring = min_plus`). The traversal executes vector-matrix products directly over the compressed sparse row representation.
- **HydraDB OpenCypher (`6.42 ms`)**: Operates over an external HTTP boundary, serializing JSON responses and persisting transactional updates over SlateDB on MinIO S3.

### B. Write Path Under Concurrent Multi-Agent Load
Where flat stores break down is **concurrent write updates**:
- When 100 agent threads attempt to record execution rewards simultaneously:
  - **SQLite**: Enforces database-level write locks (`sqlite3.OperationalError: database is locked`). Concurrency test shows p99 latency spikes above 200 ms with frequent serialization timeouts unless complex queueing layers are introduced.
  - **HydraDB**: Supports atomic in-engine edge updates (`SET p.weight = coalesce(p.weight, 1.0) + $delta`). 100 concurrent workers complete 100 consecutive `+0.15` reward updates with **zero lost updates** and final weight exactly **16.00**.

---

## 3. End-to-End Agent Latency Impact

The real performance win of Lucen is not just graph traversal speed, but the **Time-To-First-Token (TTFT)** reduction for downstream language models.

When an autonomous agent connects to 50 enterprise MCP servers:
1. **Naive Preload**: 272,607 tokens of raw JSON tool definitions are sent over the wire. The LLM must process the quadratic attention matrix over 272k tokens before generating the first token:
   - TTFT: **1,840 ms**
   - Cost: **$0.817 per turn** (at $3.00/M input tokens on Claude 3.5 Sonnet)
2. **Lucen Traversal + Filter**: Traverses the context graph in 0.21 ms (CSR) or 6.42 ms (HydraDB), prunes 496 irrelevant tools, and supplies only 4 isolated tools (1,214 total tokens):
   - TTFT: **115 ms** (15.2x faster)
   - Cost: **$0.0036 per turn** (99.6% cost reduction)

---

## 4. Hop Scaling Characteristics

We evaluated traversal latency across varying topological graph depths (1 hop to 5 hops):

| Hops | Reachable Nodes | In-Memory CSR (ms) | HydraDB Cypher (ms) | SQLite CTE (ms) |
|---|---|---|---|---|
| 1 Hop (Direct) | 4 | 0.08 ms | 4.12 ms | 0.008 ms |
| 2 Hops (Dependencies) | 18 | 0.21 ms | 6.42 ms | 0.016 ms |
| 3 Hops (Topology) | 74 | 0.44 ms | 9.38 ms | 0.062 ms |
| 4 Hops (Full Perimeter) | 210 | 0.89 ms | 14.20 ms | 0.185 ms |
| 5 Hops (Transitive Closure) | 480 | 1.45 ms | 22.10 ms | 0.420 ms |

Sparse matrix multiplication scales linearly with the number of non-zero entries (`nnz`) in the active subgraph, remaining well under human perception limits and agent network latency.
