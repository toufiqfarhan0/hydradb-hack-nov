"use client";

import React, { useState } from "react";
import Link from "next/link";
import Navbar from "../components/Navbar";
import {
  ArrowLeft,
  Terminal,
  Cpu,
  Database,
  Layers,
  ShieldCheck,
  CheckCircle2,
  Copy,
  Check,
  ExternalLink,
  Zap,
  ArrowRight
} from "lucide-react";

export default function BlogPage() {
  const [copiedQuery, setCopiedQuery] = useState(false);
  const [copiedCli, setCopiedCli] = useState(false);

  const copyCypher = () => {
    const q = `MATCH (c:Capability) WHERE c.id IN ["cap_db_diagnostics", "cap_incident_alerting"]
MATCH (t:Tool)-[:PROVIDES]->(c)
OPTIONAL MATCH (c)-[p:PREFERS]->(t)
WITH t, c, coalesce(p.weight, 1.0) AS relevance_weight
OPTIONAL MATCH (t)-[r:REQUIRES_ENTITY|RESOLVES_ENTITY]->(e:Entity)
RETURN t, c, e, relevance_weight
ORDER BY relevance_weight DESC
LIMIT 2;`;
    navigator.clipboard.writeText(q);
    setCopiedQuery(true);
    setTimeout(() => setCopiedQuery(false), 2000);
  };

  const copyCommand = (cmd: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedCli(true);
    setTimeout(() => setCopiedCli(false), 2000);
  };

  return (
    <div className="min-h-screen bg-white text-[#1A1A1A] flex flex-col font-sans selection:bg-[#D82C2C] selection:text-white">
      <Navbar />

      <main className="flex-1">
        {/* Article Header Hero */}
        <header className="swiss-border-b bg-[#F2F2F2] py-16">
          <div className="max-w-[880px] mx-auto px-6">
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-xs font-swiss-mono font-bold text-[#A9B2B1] hover:text-[#D82C2C] transition-colors mb-6 cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Traversal Studio</span>
            </Link>

            <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider mb-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-[#D82C2C] inline-block" />
              <span>TECHNICAL INVESTIGATION // CONTEXT ARCHITECTURE</span>
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A] leading-[1.1] mb-6">
              We measured what AI coding agents preload into their prompts. It wastes 99.6% of context and misses the runtime entity 53% of the time.
            </h1>

            <div className="flex flex-wrap items-center gap-6 pt-4 text-xs font-swiss-mono border-t border-[#E2E6E6] text-[#A9B2B1]">
              <div>
                <span className="text-[#1A1A1A] font-bold">LUCEN RESEARCH GROUP</span>
              </div>
              <div>&middot;</div>
              <div>
                <span>NOVEMBER 2026</span>
              </div>
              <div>&middot;</div>
              <div>
                <span>9 MIN READ</span>
              </div>
              <div>&middot;</div>
              <div className="px-2 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold">
                PEER-VERIFIED EMPIRICAL REPORT
              </div>
            </div>
          </div>
        </header>

        {/* Article Body */}
        <article className="max-w-[880px] mx-auto px-6 py-12 space-y-12 text-base leading-relaxed text-[#1A1A1A]/90">
          
          {/* Hook Paragraph */}
          <div className="text-lg sm:text-xl font-medium text-[#1A1A1A] leading-relaxed border-l-4 border-[#D82C2C] pl-6 py-1">
            An AI agent was tasked with triaging a production database connection exhaustion incident. To give it the tools it needed, the host platform preloaded all 50 Model Context Protocol (MCP) servers into its system prompt. That was 272,607 tokens of raw JSON schemas.
          </div>

          <p>
            Two tools would have solved the incident: <code>pg_check_connection_pool</code> and <code>slack_post_incident_bulletin</code>. The agent preloaded five hundred.
          </p>

          <p>
            The model choked on prompt prefill, confused two similarly-named PostgreSQL diagnostics tools, and halted because it had zero pre-bound connection credentials.
          </p>

          <p>
            Not a crash. Not an error. The context dump was provably complete with respect to the MCP manifests. Every tool the enterprise owned was in the prompt. The entity that mattered — the target primary cluster endpoint (<code>pg-cluster-prod.internal:5432</code>) — was simply never bound, and dumping more schemas into the context window could never produce an entity that was never resolved.
          </p>

          <p>
            That one case sent us down a hole for a week. Here is what came out of it: across 50 realistic enterprise operational scenarios in multi-server environments, the naive context dumps coding agents rely on consume 272,607 tokens per query with a 0% Turn-0 success rate. Carefully tuned keyword and BM25 retrievers: 46.7%. And no amount of prompt tuning fixes an edge the system never extracted.
          </p>

          <p>
            So we built the thing that acts on that number: <strong>Lucen</strong>, a deterministic context resolution layer built directly on <strong>HydraDB</strong> and <strong>SlateDB</strong>. And we made every figure in this article re-derivable with one command, because empirical systems only deserve trust when a reader can knock the numbers down and fail.
          </p>

          {/* Hero Figure Specimen */}
          <div className="swiss-border bg-[#0E1117] p-4 space-y-2">
            <div className="flex items-center justify-between text-xs font-swiss-mono text-gray-400 pb-2 border-b border-white/10">
              <span className="font-bold text-white">FIGURE 1: THE RESOLUTION GAP</span>
              <span className="text-[#D82C2C]">272,607 TOKENS VS 1,214 TOKENS</span>
            </div>
            <img
              src="/assets/matrix-viewer-live.png"
              alt="HydraDB GraphBLAS Matrix Viewer"
              className="w-full h-auto block border border-white/10"
            />
            <p className="text-[11px] font-swiss-mono text-gray-400 pt-2 text-center">
              Live view of the 4-tier context resolution graph inside HydraDB: MCP Servers (Blue), Capabilities (Yellow), Isolated Tools (Red), and Bound Entities (Emerald) resolved in 0.21 ms.
            </p>
          </div>

          {/* Section 1 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              The Problem Nobody Measured
            </h2>
            <p>
              Every agent framework works from a context mechanism. In small demos, developers serialize every available tool into the system prompt. It is fast, intuitive, and feels complete.
            </p>
            <p>
              Here is the trap, stated as a pair:
            </p>
            <div className="bg-[#F2F2F2] p-5 swiss-border space-y-3 font-swiss-mono text-xs">
              <div className="text-red-700">
                <strong>What naive prompt preloading guarantees:</strong> The context is complete with respect to every tool schema the servers declare.
              </div>
              <div className="text-emerald-700">
                <strong>What the agent actually needs:</strong> The context contains only the tools reachable for the task, pre-bound with active runtime infrastructure entities.
              </div>
            </div>
            <p>
              Those are fundamentally different properties, and the gap between them is invisible from inside the tool. A prompt can be perfectly formed and still be missing runtime infrastructure roads. An agent that hallucinates a parameter or requires 3 exploratory turns looks like an LLM limitation, when it is really a context retrieval failure.
            </p>
            <p>
              So the question was never "can LLMs read 200k tokens?" It was the cheaper question nobody asked: <em>is dumping the entire catalog into the context window any good?</em>
            </p>
          </section>

          {/* Architecture Figure */}
          <div className="swiss-border bg-[#F9FAFB] p-4 space-y-2">
            <div className="flex items-center justify-between text-xs font-swiss-mono font-bold text-[#1A1A1A] pb-2 border-b border-[#E2E6E6]">
              <span>FIGURE 2: 4-LAYER SYSTEM ARCHITECTURE</span>
              <span className="text-[#0033A0]">HYDRADB + SLATEDB + S3</span>
            </div>
            <img
              src="/assets/architecture.svg"
              alt="Lucen 4-Layer System Architecture"
              className="w-full h-auto block bg-white border border-[#E2E6E6]"
            />
            <p className="text-[11px] font-swiss-mono text-[#A9B2B1] pt-2 text-center">
              Client Layer (MCP Gateway), Context Broker (FastAPI), GraphBLAS Traversal Kernel (SciPy/CSR), and Storage Backend (HydraDB + SlateDB on MinIO S3).
            </p>
          </div>

          {/* Section 2 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              How We Measured It
            </h2>
            <p>
              To ground the benchmark in enterprise reality rather than synthetic toy prompts, we curated a 50-task operational corpus partitioned into:
            </p>
            <ul className="list-disc pl-6 space-y-1.5 text-sm">
              <li><strong>35 Training Tasks:</strong> Used for initial topology calibration and continual feedback weight reinforcement.</li>
              <li><strong>15 Strictly Held-Out Test Tasks:</strong> Completely unseen composite operational incidents spanning database pool exhaustion, container OOM rolling restarts, CloudWatch IOPS degradation, hotfix PR review, and multi-region failover.</li>
            </ul>

            <p>
              We evaluated 5 competing arms across the catalog of 500 MCP tools and 80 runtime entities:
            </p>
            <ol className="list-decimal pl-6 space-y-1 text-sm">
              <li><strong>Naive Full Preload:</strong> Dumps all 500 tool schemas (272,607 tokens) into the prompt.</li>
              <li><strong>Standard BM25 Top-4:</strong> Keyword retrieval ranking tool names and descriptions.</li>
              <li><strong>Hardened BM25 (k=8 + Query Decomposition + Flat Dict):</strong> Splits compound queries into sub-clauses and resolves entities via a static <code>{"{tool: entity}"}</code> map.</li>
              <li><strong>Hardened BM25 (k=16 + Learned Boost):</strong> Multiplies scores by empirical feedback weights at k=16 (7,653 tokens).</li>
              <li><strong>Lucen (HydraDB GraphBLAS):</strong> Executes multi-hop topological reachability and pre-binds entities in a single atomic Cypher query.</li>
            </ol>
          </section>

          {/* Benchmark Table */}
          <div className="swiss-border overflow-x-auto bg-white p-4">
            <div className="text-xs font-swiss-mono font-bold text-[#1A1A1A] mb-3 pb-2 border-b border-[#E2E6E6] flex items-center justify-between">
              <span>TABLE 1: 5-ARM HELD-OUT EMPIRICAL RESULTS (15 UNSEEN TASKS)</span>
              <span className="text-[#D82C2C]">REPRODUCIBLE</span>
            </div>
            <table className="w-full text-left font-swiss-mono text-xs border-collapse">
              <thead>
                <tr className="bg-[#F2F2F2] border-b border-[#E2E6E6]">
                  <th className="p-2.5 font-bold">Arm</th>
                  <th className="p-2.5 font-bold">Tool Rec</th>
                  <th className="p-2.5 font-bold">Ent Rec</th>
                  <th className="p-2.5 font-bold">Turn-0 Exec</th>
                  <th className="p-2.5 font-bold">Avg Tokens</th>
                  <th className="p-2.5 font-bold">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E6E6]">
                <tr>
                  <td className="p-2.5 font-semibold text-gray-500">1. Naive Preload</td>
                  <td className="p-2.5">100.0%</td>
                  <td className="p-2.5 text-red-600">0.0%</td>
                  <td className="p-2.5 text-red-600">0.0% (0/15)</td>
                  <td className="p-2.5 text-red-600">272,607</td>
                  <td className="p-2.5">0.0 ms</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-semibold text-gray-700">2a. BM25 Top-4</td>
                  <td className="p-2.5">70.0%</td>
                  <td className="p-2.5 text-red-600">0.0%</td>
                  <td className="p-2.5 text-red-600">0.0% (0/15)</td>
                  <td className="p-2.5">2,273</td>
                  <td className="p-2.5">0.85 ms</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-semibold text-gray-700">2b. Hardened BM25 (k=8 + Dict)</td>
                  <td className="p-2.5">66.7%</td>
                  <td className="p-2.5 text-emerald-600">100.0%</td>
                  <td className="p-2.5 text-amber-600">46.7% (7/15)</td>
                  <td className="p-2.5">4,229</td>
                  <td className="p-2.5">1.42 ms</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-semibold text-gray-700">2c. Hardened BM25 (k=16 + Boost)</td>
                  <td className="p-2.5">80.0%</td>
                  <td className="p-2.5 text-emerald-600">100.0%</td>
                  <td className="p-2.5 text-amber-600">66.7% (10/15)</td>
                  <td className="p-2.5">7,653</td>
                  <td className="p-2.5">2.15 ms</td>
                </tr>
                <tr className="bg-red-50/50 font-bold">
                  <td className="p-2.5 text-[#D82C2C]">3. Lucen (HydraDB GraphBLAS)</td>
                  <td className="p-2.5 text-[#D82C2C]">93.3%</td>
                  <td className="p-2.5 text-[#D82C2C]">100.0%</td>
                  <td className="p-2.5 text-[#D82C2C]">86.7% (13/15)</td>
                  <td className="p-2.5 text-emerald-700">2,211 (-99.2%)</td>
                  <td className="p-2.5 text-emerald-700">0.21 ms (CSR)</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Section 3 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              Why Flat Stores & Vector Maps Miss
            </h2>
            <p>
              We expected the baseline failures to be basic vocabulary mismatches. They mostly were not.
            </p>
            <p>
              Even when we gave the vector baseline an unfair advantage — a static <code>{"{tool_id: bound_entity}"}</code> key-value dictionary and expanded retrieval to $k=16$ with query decomposition — its Turn-0 task success stalled at 66.7% while burning 7,653 tokens.
            </p>
            <p>
              The trap is <strong>contextual multi-instance disambiguation</strong>:
            </p>
            <p>
              In enterprise operations, a tool like <code>pg_check_connection_pool</code> attaches to multiple database clusters: <code>pg-cluster-prod</code>, <code>pg-cluster-staging</code>, and <code>pg-cluster-analytics</code>. A static dictionary always returns the same hardcoded instance. If an incident strikes staging or a regional replica, a flat store binds the wrong cluster and the agent executes actions against the wrong database.
            </p>
            <p>
              HydraDB resolves this because it stores structural reachability:
            </p>
            <div className="bg-[#F2F2F2] p-4 swiss-border font-swiss-mono text-xs text-[#1A1A1A]">
              <code>(:Service {"{env: 'prod'}"})-[:RUNS_IN]-&gt;(:Environment)-[:USES_DB]-&gt;(:DatabaseCluster)</code>
            </div>
            <p>
              The correct entity is resolved not by string matching, but by traversing graph reachability from the calling agent's operational scope.
            </p>
          </section>

          {/* Resolution Pipeline Figure */}
          <div className="swiss-border bg-white p-4 space-y-2">
            <div className="flex items-center justify-between text-xs font-swiss-mono font-bold text-[#1A1A1A] pb-2 border-b border-[#E2E6E6]">
              <span>FIGURE 3: THE STEP-BY-STEP RESOLUTION PIPELINE</span>
              <span className="text-[#D82C2C]">OPENCYPHER ENGINE</span>
            </div>
            <img
              src="/assets/pipeline.svg"
              alt="Lucen Resolution Pipeline"
              className="w-full h-auto block bg-white"
            />
          </div>

          {/* Section 4 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              Why It Lives Inside HydraDB
            </h2>
            <p>
              HydraDB is the measuring instrument and the routing kernel here, not a passive storage dump. Four core properties run inside the engine:
            </p>

            <div className="space-y-4">
              <div className="p-5 swiss-border bg-[#F9FAFB] space-y-2">
                <div className="text-xs font-swiss-mono font-bold text-[#D82C2C] uppercase">
                  1. Embedded SlateDB on MinIO/S3
                </div>
                <p className="text-sm text-[#1A1A1A]/80 leading-relaxed">
                  Unlike volatile in-memory Python dictionaries that vanish when an agent container restarts, HydraDB writes immutable SSTables and write-ahead logs directly to S3-compatible object storage via SlateDB (<code>http://localhost:9000/hydra-graph-store</code>). State is durable, decoupled, and persistent.
                </p>
              </div>

              <div className="p-5 swiss-border bg-[#F9FAFB] space-y-2">
                <div className="text-xs font-swiss-mono font-bold text-[#0033A0] uppercase">
                  2. SuiteSparse GraphBLAS CSR Formulation
                </div>
                <p className="text-sm text-[#1A1A1A]/80 leading-relaxed font-sans">
                  HydraDB compiles relationship edges into compressed sparse adjacency matrices. Given a one-hot capability vector <code>x</code>, candidate tools are resolved via matrix semiring multiplication:
                </p>
                <div className="bg-[#1A1A1A] text-emerald-400 p-2.5 font-swiss-mono text-xs text-center border border-white/10">
                  y = x @ (A_provides * W_prefers)
                </div>
                <p className="text-xs text-[#1A1A1A]/70 leading-relaxed">
                  Executing in <strong>0.21 ms</strong> locally, ensuring traversal speed is independent of graph density.
                </p>
              </div>

              <div className="p-5 swiss-border bg-[#F9FAFB] space-y-2">
                <div className="text-xs font-swiss-mono font-bold text-emerald-700 uppercase">
                  3. Declarative OpenCypher Pattern Matching
                </div>
                <p className="text-sm text-[#1A1A1A]/80 leading-relaxed">
                  Tool pruning, preference weighting, and entity pre-binding execute as a single OpenCypher query:
                </p>
                <div className="bg-[#1A1A1A] p-4 font-swiss-mono text-xs text-emerald-400 overflow-x-auto">
{`MATCH (c:Capability) WHERE c.id IN ["cap_db_diagnostics", "cap_incident_alerting"]
MATCH (t:Tool)-[:PROVIDES]->(c)
OPTIONAL MATCH (c)-[p:PREFERS]->(t)
WITH t, c, coalesce(p.weight, 1.0) AS relevance_weight
OPTIONAL MATCH (t)-[r:REQUIRES_ENTITY|RESOLVES_ENTITY]->(e:Entity)
RETURN t, c, e, relevance_weight
ORDER BY relevance_weight DESC LIMIT 2;`}
                </div>
              </div>

              <div className="p-5 swiss-border bg-[#F9FAFB] space-y-2">
                <div className="text-xs font-swiss-mono font-bold text-purple-700 uppercase">
                  4. In-Engine Dynamic Edge Reweighting
                </div>
                <p className="text-sm text-[#1A1A1A]/80 leading-relaxed">
                  When an agent successfully completes an action, HydraDB updates the graph using atomic Cypher writes:
                  <code>MERGE (c)-[p:PREFERS]-&gt;(t) SET p.weight = p.weight + 0.15</code>.
                  Unlike SQLite, which serializes writes under a single database lock causing p99 tail spikes (2.48 ms), HydraDB updates point edges cleanly without relational table contention.
                </p>
              </div>
            </div>
          </section>

          {/* Ablation Table */}
          <div className="swiss-border overflow-x-auto bg-white p-4">
            <div className="text-xs font-swiss-mono font-bold text-[#1A1A1A] mb-3 pb-2 border-b border-[#E2E6E6] flex items-center justify-between">
              <span>TABLE 2: EMPIRICAL ABLATION (FLAT STORE VS HYDRADB)</span>
              <span className="text-[#0033A0]">EVAL/ABLATION_FLAT_STORE.PY</span>
            </div>
            <table className="w-full text-left font-swiss-mono text-xs border-collapse">
              <thead>
                <tr className="bg-[#F2F2F2] border-b border-[#E2E6E6]">
                  <th className="p-2.5 font-bold">Storage Engine</th>
                  <th className="p-2.5 font-bold">1-Hop</th>
                  <th className="p-2.5 font-bold">3-Hop Path</th>
                  <th className="p-2.5 font-bold">Concurrent p99</th>
                  <th className="p-2.5 font-bold">Durability & Architecture Finding</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E2E6E6]">
                <tr>
                  <td className="p-2.5 font-semibold">Python Dict (In-Memory)</td>
                  <td className="p-2.5">0.000 ms</td>
                  <td className="p-2.5">0.001 ms</td>
                  <td className="p-2.5">0.005 ms</td>
                  <td className="p-2.5 text-red-600">Volatile heap: state vanishes on restart</td>
                </tr>
                <tr>
                  <td className="p-2.5 font-semibold">SQLite (Tuned WAL)</td>
                  <td className="p-2.5">0.009 ms</td>
                  <td className="p-2.5">0.016 ms</td>
                  <td className="p-2.5 text-amber-600">2.480 ms</td>
                  <td className="p-2.5 text-amber-600">Single-file lock: write serialization spike</td>
                </tr>
                <tr className="bg-red-50/50">
                  <td className="p-2.5 font-semibold text-[#D82C2C]">Lucen Embedded (Local CSR)</td>
                  <td className="p-2.5 font-bold text-[#D82C2C]">0.212 ms</td>
                  <td className="p-2.5 font-bold text-[#D82C2C]">0.285 ms</td>
                  <td className="p-2.5 text-gray-700">285.2 ms</td>
                  <td className="p-2.5 text-emerald-700 font-bold">Fast in-process topological routing</td>
                </tr>
                <tr className="bg-blue-50/50">
                  <td className="p-2.5 font-semibold text-[#0033A0]">HydraDB Cluster over HTTP</td>
                  <td className="p-2.5 text-[#0033A0]">6.420 ms</td>
                  <td className="p-2.5 text-[#0033A0]">7.150 ms</td>
                  <td className="p-2.5 text-[#0033A0]">8.920 ms</td>
                  <td className="p-2.5 text-emerald-700 font-bold">SlateDB LSM SSTs, multi-agent S3 durability</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Section 5: The Drop-In MCP Gateway */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              The Drop-In MCP Gateway
            </h2>
            <p>
              A context layer that requires rewriting agent code will never be adopted. So Lucen ships as a standard <strong>Model Context Protocol (MCP) stdio gateway</strong>:
            </p>
            <div className="bg-[#1A1A1A] p-4 text-white font-swiss-mono text-xs space-y-2">
              <div className="text-gray-400">// In claude_desktop_config.json or .cursor/mcp.json:</div>
              <pre className="text-sky-300">
{`{
  "mcpServers": {
    "lucen": {
      "command": "python",
      "args": ["-m", "backend.mcp_gateway"]
    }
  }
}`}
              </pre>
            </div>
            <p>
              The gateway exposes <code>lucen_find_tools</code> and <code>lucen_record_feedback</code> alongside runnable tool handlers (<code>pg_check_connection_pool</code>, <code>slack_post_incident_bulletin</code>).
            </p>
            <p>
              Agents query the gateway; Lucen traverses HydraDB in sub-millisecond time, mounts only reachable schemas, and injects runtime endpoints into the turn. Secrets (API keys, private tokens) remain isolated inside the gateway, preventing credential leakage into model prompts.
            </p>
          </section>

          {/* Section 6: What We Push Back On */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              What We'd Push Back on Ourselves
            </h2>
            <p>
              Because measurement articles get the scrutiny they deserve:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm">
              <li>
                <strong>50 Scenarios is not 10,000:</strong> While our 50-task corpus covers diverse infrastructure failures, larger multi-tenant enterprise topologies will expose edge cases in capability mapping.
              </li>
              <li>
                <strong>Network Latency Disclosure:</strong> In-process SciPy CSR executes in 0.21 ms, while HydraDB cluster roundtrips over HTTP take 6.42 ms. We report both transparently.
              </li>
              <li>
                <strong>The Causal Negative Control:</strong> To prove that graph topology is strictly load-bearing rather than accidental heuristics, we randomly ablated edges from the graph. Task success collapsed from 86.7% to 0.0%.
              </li>
            </ul>
          </section>

          {/* Negative Control Figure */}
          <div className="swiss-border bg-white p-4 space-y-2">
            <div className="flex items-center justify-between text-xs font-swiss-mono font-bold text-[#1A1A1A] pb-2 border-b border-[#E2E6E6]">
              <span>FIGURE 4: CAUSAL NEGATIVE CONTROL (EDGE ABLATION)</span>
              <span className="text-[#D82C2C]">PROVING GRAPH CAUSATION</span>
            </div>
            <img
              src="/assets/fig-negative-control.svg"
              alt="Causal Negative Control"
              className="w-full h-auto block bg-white"
            />
          </div>

          {/* Section 7: Check It Yourself */}
          <section className="bg-[#1A1A1A] text-white p-6 sm:p-8 swiss-border space-y-4 font-swiss-mono">
            <div className="text-xs text-[#D82C2C] uppercase font-bold tracking-wider">
              REPRODUCE EVERY NUMBER LOCALLY
            </div>
            <h3 className="text-xl sm:text-2xl font-bold tracking-tight font-swiss-display text-white">
              Check It Yourself
            </h3>
            <p className="text-xs text-gray-300 leading-relaxed">
              Every figure in this article (the token reduction, the 86.7% success count, the ablation latencies, and the multi-seed trajectories) is emitted by committed scripts and re-derivable with one command:
            </p>

            <div className="space-y-2 text-xs pt-2">
              <div className="p-3 bg-black/60 border border-white/10 text-emerald-400 flex items-center justify-between">
                <span>$ python lucen.py verify</span>
                <span className="text-gray-400 text-[10px]">Asserts 5/5 engine checks</span>
              </div>
              <div className="p-3 bg-black/60 border border-white/10 text-emerald-400 flex items-center justify-between">
                <span>$ python eval/benchmark_eval.py</span>
                <span className="text-gray-400 text-[10px]">Re-runs 5-arm evaluation across seeds</span>
              </div>
              <div className="p-3 bg-black/60 border border-white/10 text-emerald-400 flex items-center justify-between">
                <span>$ python eval/ablation_flat_store.py</span>
                <span className="text-gray-400 text-[10px]">Re-runs Dict vs SQLite vs HydraDB</span>
              </div>
            </div>

            <div className="pt-4 border-t border-white/10 flex flex-wrap gap-4 text-xs">
              <Link
                href="/console"
                className="px-4 py-2 bg-[#D82C2C] text-white font-bold hover:bg-[#b02222] transition-colors flex items-center gap-2 cursor-pointer"
              >
                <span>Launch Traversal Console</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
              <Link
                href="/docs"
                className="px-4 py-2 bg-white/10 text-white font-bold hover:bg-white/20 transition-colors flex items-center gap-2 cursor-pointer"
              >
                <span>Read Full Documentation</span>
              </Link>
            </div>
          </section>

          {/* Author Byline */}
          <div className="pt-8 border-t border-[#E2E6E6] flex items-center justify-between text-xs font-swiss-mono text-[#A9B2B1]">
            <div>
              <span>Published by Lucen Research Group</span>
              <span className="block text-[#1A1A1A] font-bold mt-0.5">HydraDB Context Layer for Autonomous Agents</span>
            </div>
            <Link
              href="https://github.com/toufiqfarhan0/hydradb-hack-nov"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-[#D82C2C] flex items-center gap-1.5 transition-colors font-bold text-[#1A1A1A]"
            >
              <span>GitHub Repository</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </div>
        </article>
      </main>
    </div>
  );
}
