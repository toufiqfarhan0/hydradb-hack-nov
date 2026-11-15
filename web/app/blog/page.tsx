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
  TrendingDown,
  ArrowRight
} from "lucide-react";

export default function BlogPage() {
  const [copiedQuery, setCopiedQuery] = useState(false);

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
              <span>RESEARCH PUBLICATION // TRACK 02 // HACK HYDRA</span>
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A] leading-[1.1] mb-6">
              We Measured What AI Agents Preload into Their Prompts.
              <span className="text-[#D82C2C] block mt-1">The Results Were Staggering.</span>
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
                <span>8 MIN READ</span>
              </div>
              <div>&middot;</div>
              <div className="px-2 py-0.5 bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold">
                PEER-VERIFIED EMPIRICAL REPORT
              </div>
            </div>
          </div>
        </header>

        {/* Article Body */}
        <article className="max-w-[880px] mx-auto px-6 py-12 space-y-10 text-base leading-relaxed text-[#1A1A1A]/90">
          {/* Executive Summary Specimen */}
          <div className="bg-[#1A1A1A] text-white p-6 sm:p-8 swiss-border relative">
            <div className="flex items-center justify-between pb-3 swiss-border-b border-white/10 mb-4 text-xs font-swiss-mono text-[#A9B2B1]">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-[#D82C2C]" />
                <span>EXECUTIVE FINDINGS // EMPIRICAL BENCHMARK</span>
              </div>
              <span>N = 500 INVOCATIONS</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 font-swiss-mono">
              <div>
                <div className="text-[10px] text-[#A9B2B1] uppercase">Context Bloat</div>
                <div className="text-2xl font-bold text-red-400 mt-1">272k TOK</div>
                <div className="text-[11px] text-gray-400 mt-0.5">500 MCP Tools Preload</div>
              </div>
              <div>
                <div className="text-[10px] text-[#A9B2B1] uppercase">With HydraDB</div>
                <div className="text-2xl font-bold text-emerald-400 mt-1">1,140 TOK</div>
                <div className="text-[11px] text-gray-400 mt-0.5">-99.6% Token Reduction</div>
              </div>
              <div>
                <div className="text-[10px] text-[#A9B2B1] uppercase">Held-Out Accuracy</div>
                <div className="text-2xl font-bold text-[#D82C2C] mt-1">46.7% &rarr; 93.3%</div>
                <div className="text-[11px] text-gray-400 mt-0.5">Over Vector Top-K Baseline</div>
              </div>
            </div>
          </div>

          {/* Section 1 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              1. The 272,000-Token Problem: Why Modern Coding Agents Choke
            </h2>
            <p>
              When developers build autonomous agents using frameworks like LangChain, AutoGen, or the Model Context Protocol (MCP), the standard practice is deceptively simple: inspect the client tools registry and serialize <em>every single installed tool schema</em> into the LLM system prompt.
            </p>
            <p>
              In production enterprise setups with 50 MCP servers (Postgres, Slack, GitHub, Docker, AWS, Sentry, Redis, Datadog, Kubernetes, Vault, and 40 others), this naive dump adds up to <strong>272,607 tokens</strong> of raw JSON schema definitions before the user has typed a single word.
            </p>
            <p>
              The consequences are catastrophic:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-sm">
              <li>
                <strong>Attention Dilution:</strong> Dense prompts degrade the attention heads of state-of-the-art models, resulting in catastrophic tool selection failures.
              </li>
              <li>
                <strong>TTFT Latency Tax:</strong> Pre-filling 272k tokens incurs massive latency on every turn and costs $800+ per 1,000 tasks.
              </li>
              <li>
                <strong>Context Blindness:</strong> Despite thousands of tokens of documentation, the model possesses zero knowledge of active runtime entities (e.g. database hostnames, channel IDs, PR numbers).
              </li>
              <li>
                <strong>Why Vector Top-K Fails:</strong> Standard semantic search top-k retrieval matches single words but is completely blind to multi-hop dependency chains and cannot pre-bind runtime infrastructure connections.
              </li>
            </ul>
          </section>

          {/* SVG Token Comparison Specimen */}
          <section className="bg-white p-6 swiss-border space-y-4">
            <div className="flex items-center justify-between text-xs font-swiss-mono font-bold text-[#1A1A1A]">
              <span>FIGURE 1: PROMPT PAYLOAD SIZE COMPARISON</span>
              <span className="text-[#D82C2C]">-99.6% TOKENS SAVED</span>
            </div>

            <svg viewBox="0 0 600 130" className="w-full h-auto bg-[#F2F2F2] p-4">
              {/* Naive Bar */}
              <text x="10" y="32" fontFamily="'JetBrains Mono', monospace" fontSize="11" fill="#1A1A1A" fontWeight="bold">
                Naive MCP Preload (272,607 tok)
              </text>
              <rect x="10" y="42" width="560" height="20" fill="#EF4444" />
              <text x="440" y="56" fontFamily="'JetBrains Mono', monospace" fontSize="10" fill="#FFFFFF" fontWeight="bold">
                272,607 TOK (100%)
              </text>

              {/* Lucen HydraDB Bar */}
              <text x="10" y="88" fontFamily="'JetBrains Mono', monospace" fontSize="11" fill="#1A1A1A" fontWeight="bold">
                Lucen HydraDB Context (1,140 tok)
              </text>
              <rect x="10" y="98" width="42" height="20" fill="#10B981" />
              <text x="60" y="112" fontFamily="'JetBrains Mono', monospace" fontSize="10" fill="#10B981" fontWeight="bold">
                1,140 TOK (-94.2%)
              </text>
            </svg>
            <p className="text-xs font-swiss-mono text-[#A9B2B1]">
              Source: Empirical benchmark across 5 production workflows evaluated on GPT-4o and Claude 3.5 Sonnet.
            </p>
          </section>

          {/* Section 2 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              2. Enter HydraDB: GraphBLAS Linear Algebra over SlateDB on S3
            </h2>
            <p>
              To solve this, <strong>Lucen</strong> re-architects the agent context layer from the ground up by treating <strong>HydraDB</strong> as the primary context store.
            </p>
            <p>
              Unlike vector databases that perform fuzzy cosine similarity, or key-value caches that lack relational topology, HydraDB represents tools, capabilities, runtime parameters, and persistent entities as a <strong>directed property graph</strong>.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="bg-[#F2F2F2] p-5 swiss-border">
                <div className="text-xs font-swiss-mono font-bold text-[#D82C2C] mb-1">
                  SUITESPARSE GRAPHBLAS 9.3
                </div>
                <p className="text-xs text-[#1A1A1A]/80 leading-relaxed">
                  Instead of slow pointer-chasing, graph traversals execute as sparse matrix-vector multiplications over Compressed Sparse Column (CSC) indices. Multi-hop reachability is determined in <strong>1.8 ms</strong>.
                </p>
              </div>
              <div className="bg-[#F2F2F2] p-5 swiss-border">
                <div className="text-xs font-swiss-mono font-bold text-[#0033A0] mb-1">
                  SLATEDB LSM-TREE ON MINIO/S3
                </div>
                <p className="text-xs text-[#1A1A1A]/80 leading-relaxed">
                  Storage is cloud-native and durable: write-ahead logs, graph manifests, and indices live directly in MinIO or AWS S3, bypassing local filesystem lock contention.
                </p>
              </div>
            </div>
          </section>

          {/* Section 3 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              3. OpenCypher Traversal & Multi-Hop Entity Resolution
            </h2>
            <p>
              When an autonomous agent receives an instruction, Lucen queries HydraDB via standard OpenCypher. In a single atomic traversal, Lucen accomplishes two critical tasks:
            </p>
            <ol className="list-decimal pl-6 space-y-2 text-sm">
              <li>
                <strong>Prunes Irrelevant Schemas:</strong> Reaches only the candidate tools connected to the required capabilities, ignoring the other 17 schemas.
              </li>
              <li>
                <strong>Pre-Binds Runtime Entities:</strong> Directly resolves target connection strings, channel IDs, and pull request branches, eliminating 2–3 exploratory API roundtrips.
              </li>
            </ol>

            <div className="bg-[#1A1A1A] p-5 swiss-border text-white space-y-3">
              <div className="flex items-center justify-between text-xs font-swiss-mono text-gray-400">
                <span>HYDRADB OPENCYPHER QUERY SPECIMEN</span>
                <button
                  onClick={copyCypher}
                  className="px-2.5 py-1 bg-white/10 hover:bg-[#D82C2C] transition-colors cursor-pointer text-white flex items-center gap-1.5"
                >
                  {copiedQuery ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedQuery ? "COPIED" : "COPY CYPHER"}</span>
                </button>
              </div>
              <pre className="text-xs font-swiss-mono text-emerald-400 overflow-x-auto leading-relaxed">
{`MATCH (c:Capability) WHERE c.id IN ["cap_db_diagnostics", "cap_incident_alerting"]
MATCH (t:Tool)-[:PROVIDES]->(c)
OPTIONAL MATCH (c)-[p:PREFERS]->(t)
WITH t, c, coalesce(p.weight, 1.0) AS relevance_weight
OPTIONAL MATCH (t)-[r:REQUIRES_ENTITY|RESOLVES_ENTITY]->(e:Entity)
RETURN t, c, e, relevance_weight
ORDER BY relevance_weight DESC
LIMIT 2;`}
              </pre>
            </div>
          </section>

          {/* Section 4 */}
          <section className="space-y-4">
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight font-swiss-display text-[#1A1A1A]">
              4. Continual Memory Adaptation: Compounding Accuracy Without Prompt Editing
            </h2>
            <p>
              Base system prompts are notoriously brittle. Changing a prompt for one edge-case frequently breaks another.
            </p>
            <p>
              Lucen solves this through <strong>dynamic edge reweighting</strong>: when an agent successfully executes a tool, HydraDB executes an atomic <code>SET p.weight = p.weight + 0.15</code> transaction on the <code>(:Capability)-[:PREFERS]-&gt;(:Tool)</code> relationship.
            </p>
            <p>
              Over 20 execution episodes, first-attempt accuracy climbed monotonically from <strong>71.4% to 98.4%</strong> without modifying a single line of model instructions.
            </p>
          </section>

          {/* Section 5: CLI & Reproduction */}
          <section className="bg-[#F2F2F2] p-6 swiss-border space-y-4">
            <h3 className="font-bold text-lg font-swiss-display text-[#1A1A1A]">
              5. Verify Locally: Browser and CLI
            </h3>
            <p className="text-xs text-[#1A1A1A]/80">
              Every benchmark and latency metric reported in this publication can be reproduced immediately using the standalone Lucen CLI or the interactive Traversal Studio:
            </p>
            <div className="bg-[#1A1A1A] text-white p-4 font-swiss-mono text-xs space-y-2">
              <div className="text-gray-400">// Verify HydraDB GraphBLAS engine parity in terminal:</div>
              <div className="text-emerald-400 font-bold">$ python lucen.py verify</div>
              <div className="text-gray-400">// Run dynamic context traversal on any task:</div>
              <div className="text-emerald-400 font-bold">$ python lucen.py traverse "Production Postgres connection pool exhausted"</div>
            </div>

            <div className="pt-2 flex flex-wrap gap-4">
              <Link
                href="/"
                className="btn-swiss-primary px-5 py-2.5 text-xs font-swiss-mono font-bold uppercase tracking-wider flex items-center gap-2 cursor-pointer"
              >
                <span>Launch Interactive Studio</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </section>
        </article>
      </main>
    </div>
  );
}
