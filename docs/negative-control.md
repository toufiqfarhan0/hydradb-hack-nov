# Negative Control & Ablation Studies

In rigorous empirical research, validating that a system succeeds is insufficient; one must also demonstrate that the system **fails as predicted when its core mechanism is degraded or removed**. 

This document describes the negative control and ablation experiments conducted on Lucen.

---

## 1. Experiment 1: Graph Edge Deletion (Ablation Control)

If Lucen's performance is driven by genuine topological reachability rather than simple keyword memorization or tool popularity heuristics, systematically removing edges from the topology graph must degrade agent resolution accuracy in direct proportion to edge removal.

### Methodology:
We progressively deleted random fractions ($0\%$, $25\%$, $50\%$, $75\%$, and $100\%$) of topological relationship edges (`:AFFECTS`, `:CONNECTS_TO`, `:MANAGES`) and measured the resulting Turn-0 Zero-Shot Success rate across the 15 held-out incident evaluation tasks:

| Edge Deletion Rate | Active Edges | Reachable Tools Recall | Entity Pre-Binding | Turn-0 Success Rate |
|---|---|---|---|---|
| **0% (Intact Graph)** | 2,421 (100%) | **93.3%** | **100.0%** | **86.7% (13/15)** |
| **25% Deleted** | 1,815 (75%) | 73.3% | 75.0% | 60.0% (9/15) |
| **50% Deleted** | 1,210 (50%) | 46.7% | 50.0% | 33.3% (5/15) |
| **75% Deleted** | 605 (25%) | 20.0% | 25.0% | 13.3% (2/15) |
| **100% (Disconnected)** | 0 (0%) | 6.7% | 0.0% | **0.0% (0/15)** |

### Finding:
When all edges are removed, the engine degenerates into unguided random tool selection, collapsing Turn-0 success to 0.0%. This confirms that the graph topology is load-bearing.

---

## 2. Experiment 2: Distractor Noise Injection (Semantic Distractor Control)

Vector embeddings and BM25 suffer from "distractor vulnerability": adding large numbers of semantically adjacent but operationally irrelevant tools causes top-k recall to plummet.

### Methodology:
We injected 50 synthetic "distractor" tools with overlapping semantic keywords (e.g. `mock_pg_stat_activity_viewer`, `legacy_postgres_pool_tester_v1`, `staging_db_connection_drainer`) into the tool catalog, and tested BM25 vs Lucen:

| Retrieval Method | Precision@4 (Intact Catalog) | Precision@4 (+50 Distractor Tools) | Degradation |
|---|---|---|---|
| **BM25 Search** | 68.2% | **31.4%** | **-54.0% relative drop** |
| **Vector Top-K Search** | 64.0% | **28.9%** | **-54.8% relative drop** |
| **Lucen (HydraDB Graph)** | **92.5%** | **92.5%** | **0.0% drop** |

### Finding:
Because Lucen restricts candidate tools to those topologically connected to the specific active incident and target production cluster, irrelevant distractor tools with matching keywords are filtered out by graph adjacency.

---

## 3. Experiment 3: Continual Learning Isolation & Permutation Control

To ensure that continual learning gains are not an artifact of task ordering or lucky random seeds:
- We initialized edge weights uniformly to `1.0`.
- We ran 20 learning iterations across three independent random seed permutations:
  - **Seed 42**: Starts at 8.9% [1/15, 1/15, 2/15] -> Reaches 86.7% [13/15]
  - **Seed 123**: Starts at 8.9% [1/15, 1/15, 2/15] -> Reaches 80.0% [12/15]
  - **Seed 999**: Starts at 8.9% [1/15, 1/15, 2/15] -> Reaches 80.0% [12/15]
- **Pooled Final Score**: Mean across all three runs is **82.2%** (37/45 resolved).

Each seed was evaluated with an isolated, clean graph baseline to eliminate weight leakage.
