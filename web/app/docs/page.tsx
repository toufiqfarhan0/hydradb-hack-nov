"use client";

import React, { useState } from "react";
import Link from "next/link";
import Navbar from "../components/Navbar";
import {
  BookOpen,
  Terminal,
  Database,
  Layers,
  Zap,
  Code2,
  Copy,
  Check,
  ArrowRight,
  ShieldCheck,
  Sliders,
  ExternalLink,
  ChevronRight
} from "lucide-react";

interface DocSection {
  id: string;
  number: string;
  title: string;
}

const SECTIONS: DocSection[] = [
  { id: "overview", number: "01", title: "Architecture Overview" },
  { id: "quickstart", number: "02", title: "Quickstart & Setup" },
  { id: "graphblas", number: "03", title: "GraphBLAS Kernel Spec" },
  { id: "opencypher", number: "04", title: "OpenCypher Query Pipeline" },
  { id: "continual", number: "05", title: "Continual Learning Memory" },
  { id: "gateway", number: "06", title: "Drop-In MCP Gateway" },
  { id: "api", number: "07", title: "REST API Reference" },
  { id: "cli", number: "08", title: "CLI Command Reference" },
  { id: "benchmarks", number: "09", title: "Evaluation Methodology" }
];

export default function DocsPage() {
  const [activeSection, setActiveSection] = useState<string>("overview");
  const [copiedSnippet, setCopiedSnippet] = useState<string | null>(null);

  const handleCopy = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedSnippet(id);
    setTimeout(() => setCopiedSnippet(null), 2000);
  };

  return (
    <div className="min-h-screen bg-white text-[#1A1A1A] flex flex-col font-sans selection:bg-[#D82C2C] selection:text-white">
      <Navbar />

      {/* Docs Header Banner */}
      <section className="bg-[#1A1A1A] text-white py-12 px-6 swiss-border-b">
        <div className="max-w-[1400px] mx-auto">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-2 px-2.5 py-0.5 bg-[#D82C2C] text-white text-[11px] font-swiss-mono font-bold tracking-wider uppercase">
                <span>PROTOCOL SPECIFICATION // VERSION 1.2.0</span>
              </div>
              <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight font-swiss-display text-white">
                Lucen Documentation
              </h1>
              <p className="text-sm sm:text-base text-white/70 max-w-2xl font-sans">
                The deterministic GraphBLAS context resolution layer for autonomous AI agents built on HydraDB and SlateDB.
              </p>
            </div>

            <div className="flex flex-wrap gap-3">
              <a
                href="https://lucen-app.onrender.com"
                target="_blank"
                rel="noreferrer"
                className="px-4 py-2.5 bg-[#0033A0] text-white hover:bg-[#002270] font-swiss-mono text-xs font-bold transition-colors flex items-center gap-1.5"
              >
                <ExternalLink className="w-3.5 h-3.5" />
                <span>Live App (Render) &rarr;</span>
              </a>
              <Link
                href="/console"
                className="px-4 py-2.5 bg-[#D82C2C] text-white hover:bg-[#b02222] font-swiss-mono text-xs font-bold transition-colors flex items-center gap-1.5"
              >
                <Sliders className="w-3.5 h-3.5" />
                <span>Launch Console &rarr;</span>
              </Link>
              <Link
                href="/blog"
                className="px-4 py-2.5 bg-white/10 text-white hover:bg-white/20 border border-white/20 font-swiss-mono text-xs font-bold transition-colors flex items-center gap-1.5"
              >
                <span>Read Empirical Paper &rarr;</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Main Documentation Container */}
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 py-10 w-full flex-1">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          
          {/* Left Sidebar Table of Contents */}
          <aside className="lg:col-span-3 sticky top-24 bg-[#F2F2F2] p-4 swiss-border">
            <div className="text-xs font-swiss-mono font-bold text-[#D82C2C] uppercase tracking-wider mb-3 pb-2 border-b border-[#E2E6E6]">
              TABLE OF CONTENTS
            </div>
            <nav className="space-y-1 font-swiss-mono text-xs">
              {SECTIONS.map((sec) => (
                <a
                  key={sec.id}
                  href={`#${sec.id}`}
                  onClick={() => setActiveSection(sec.id)}
                  className={`flex items-center justify-between px-3 py-2 transition-colors cursor-pointer ${
                    activeSection === sec.id
                      ? "bg-[#1A1A1A] text-white font-bold"
                      : "text-[#1A1A1A]/80 hover:bg-white hover:text-[#1A1A1A]"
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <span className={activeSection === sec.id ? "text-[#D82C2C]" : "text-gray-400"}>
                      {sec.number}
                    </span>
                    <span>{sec.title}</span>
                  </span>
                  <ChevronRight className="w-3 h-3 opacity-60" />
                </a>
              ))}
            </nav>

            <div className="mt-6 pt-4 border-t border-[#E2E6E6] space-y-2 text-[11px] font-swiss-mono text-gray-600">
              <div className="flex justify-between">
                <span>INDEXED TOOLS:</span>
                <span className="font-bold text-[#1A1A1A]">500 Tools</span>
              </div>
              <div className="flex justify-between">
                <span>MCP SERVERS:</span>
                <span className="font-bold text-[#1A1A1A]">50 Servers</span>
              </div>
              <div className="flex justify-between">
                <span>GRAPH EDGES:</span>
                <span className="font-bold text-[#1A1A1A]">2,421 Edges</span>
              </div>
              <div className="flex justify-between">
                <span>HOP LATENCY:</span>
                <span className="font-bold text-[#0033A0]">1.8 ms</span>
              </div>
            </div>
          </aside>

          {/* Main Docs Content */}
          <main className="lg:col-span-9 space-y-16">
            
            {/* 01 // OVERVIEW */}
            <section id="overview" className="space-y-5 scroll-mt-24">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                01 // SYSTEM OVERVIEW
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                Why HydraDB as an Agent Context Layer?
              </h2>
              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                Modern autonomous coding agents (Claude Desktop, Cursor, LangChain, AutoGen) interact with real-world infrastructure using the Model Context Protocol (MCP). When organizations deploy 10 to 50 enterprise MCP microservices, standard frameworks make a fatal architectural compromise: <strong>they dump all 500+ tool schemas into the LLM prompt on every single turn</strong>.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-swiss-mono text-xs">
                <div className="p-4 bg-[#F2F2F2] swiss-border">
                  <div className="text-[#D82C2C] font-bold mb-1">PROMPT DUMPING</div>
                  <div className="font-bold text-sm text-[#1A1A1A]">272k Tokens Wasted</div>
                  <p className="text-[11px] text-[#1A1A1A]/70 mt-1 font-sans">
                    Serializing 500 tool schemas consumes 272,607 tokens ($817.20 / 1k tasks) and creates severe attention dilution.
                  </p>
                </div>
                <div className="p-4 bg-[#F2F2F2] swiss-border">
                  <div className="text-[#0033A0] font-bold mb-1">VECTOR TOP-K FAILURE</div>
                  <div className="font-bold text-sm text-[#1A1A1A]">53.3% Drop Rate</div>
                  <p className="text-[11px] text-[#1A1A1A]/70 mt-1 font-sans">
                    Vector search matches single words, dropping chained dependencies and retaining 0.0% entity awareness.
                  </p>
                </div>
                <div className="p-4 bg-emerald-50 border border-emerald-300">
                  <div className="text-emerald-700 font-bold mb-1">LUCEN HYDRADB</div>
                  <div className="font-bold text-sm text-emerald-900">1.8ms Resolution</div>
                  <p className="text-[11px] text-emerald-800 mt-1 font-sans">
                    GraphBLAS sparse linear algebra isolates exact tools (-99.6% tokens) and pre-binds live infrastructure entities.
                  </p>
                </div>
              </div>

              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                Lucen turns HydraDB into the primary context router. Rather than relying on static embeddings or prompt bloat, the agent queries HydraDB via declarative OpenCypher queries, executing multi-hop reachability over SuiteSparse/SciPy GraphBLAS sparse matrices in sub-2ms.
              </p>
            </section>

            {/* 02 // QUICKSTART */}
            <section id="quickstart" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                02 // GETTING STARTED
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                Quickstart &amp; Verification
              </h2>
              <p className="text-sm text-[#1A1A1A]/85">
                Lucen is completely self-contained with dual CLI and Web interfaces. It requires Python 3.10+ and Node.js 18+.
              </p>

              {/* Code block */}
              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10 relative">
                <button
                  onClick={() => handleCopy(`git clone https://github.com/toufiqfarhan0/hydradb-hack-nov.git\ncd hydradb-hack-nov\npip install -r requirements.txt\npython lucen.py verify`, "qs1")}
                  className="absolute top-3 right-3 px-2 py-1 bg-white/10 hover:bg-white/20 text-gray-300 text-[10px] flex items-center gap-1 transition-colors"
                >
                  {copiedSnippet === "qs1" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedSnippet === "qs1" ? "COPIED" : "COPY"}</span>
                </button>
                <div className="text-gray-500 mb-2">// 1. Clone repository and run automated parity verification</div>
                <pre className="text-gray-200">
{`git clone https://github.com/toufiqfarhan0/hydradb-hack-nov.git
cd hydradb-hack-nov
pip install -r requirements.txt
python lucen.py verify`}
                </pre>
              </div>

              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10 relative">
                <button
                  onClick={() => handleCopy(`python lucen.py stats\npython lucen.py traverse "Production PostgreSQL database outage on primary database cluster"`, "qs2")}
                  className="absolute top-3 right-3 px-2 py-1 bg-white/10 hover:bg-white/20 text-gray-300 text-[10px] flex items-center gap-1 transition-colors"
                >
                  {copiedSnippet === "qs2" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedSnippet === "qs2" ? "COPIED" : "COPY"}</span>
                </button>
                <div className="text-gray-500 mb-2">// 2. Execute natural language context resolution via CLI</div>
                <pre className="text-gray-200">
{`# Inspect graph topology (50 servers, 500 tools, 2,421 edges)
python lucen.py stats

# Execute sub-2ms multi-hop traversal and entity resolution
python lucen.py traverse "Production PostgreSQL database outage on primary database cluster"`}
                </pre>
              </div>

              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10 relative">
                <button
                  onClick={() => handleCopy(`cd web\nnpm install\nnpm run dev`, "qs3")}
                  className="absolute top-3 right-3 px-2 py-1 bg-white/10 hover:bg-white/20 text-gray-300 text-[10px] flex items-center gap-1 transition-colors"
                >
                  {copiedSnippet === "qs3" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedSnippet === "qs3" ? "COPIED" : "COPY"}</span>
                </button>
                <div className="text-gray-500 mb-2">// 3. Launch Swiss Modernist Web UI &amp; Console Studio</div>
                <pre className="text-gray-200">
{`cd web
npm install
npm run dev

# Open http://localhost:3000 in your browser
# Console Studio: http://localhost:3000/console
# Or access the live deployment: https://lucen-app.onrender.com`}
                </pre>
              </div>
            </section>

            {/* 03 // GRAPHBLAS KERNEL */}
            <section id="graphblas" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                03 // LINEAR ALGEBRA KERNEL
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                GraphBLAS CSR Semiring Traversal
              </h2>
              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                Traditional graph engines chase heap pointers between struct objects, creating high cache miss rates as topology scales. HydraDB structures the property graph as a Compressed Sparse Row (CSR) adjacency matrix:
              </p>

              <div className="p-4 bg-[#F2F2F2] swiss-border font-swiss-mono text-xs space-y-2">
                <div className="text-[#0033A0] font-bold">MATHEMATICAL FORMULATION // PLUS_TIMES SEMIRING:</div>
                <div className="text-[#1A1A1A] bg-white p-3 border border-[#E2E6E6]">
                  v_(k+1) = v_k &bull; A_CSR
                </div>
                <p className="text-[11px] text-gray-600 font-sans">
                  Where <code>v_0</code> is the one-hot task intent vector at matched capability node indices, and <code>A_CSR</code> is the 730x730 sparse adjacency matrix containing 2,421 directed weighted relationships.
                </p>
              </div>

              <div className="space-y-2">
                <h3 className="font-bold text-base font-swiss-display">Sparse Vector-Matrix Multiplication Benchmark:</h3>
                <ul className="list-disc pl-6 space-y-1 text-xs font-swiss-mono text-[#1A1A1A]/80">
                  <li>Matrix Dimension: <strong>730 nodes &times; 730 nodes</strong></li>
                  <li>Non-Zero Entries (nnz): <strong>2,415 weighted relationships</strong></li>
                  <li>1-Hop Vector-Matrix Multiplication: <strong>0.35 milliseconds</strong></li>
                  <li>2-Hop Multi-Hop Entity Resolution: <strong>1.80 milliseconds</strong></li>
                </ul>
              </div>
            </section>

            {/* 04 // OPENCYPHER QUERY PIPELINE */}
            <section id="opencypher" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                04 // QUERY DIALECT
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                3-Stage OpenCypher Pipeline
              </h2>
              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                Every agent natural language turn compiles into a deterministic 3-stage OpenCypher query executed with snapshot read consistency over SlateDB:
              </p>

              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10 relative">
                <button
                  onClick={() => handleCopy(`// Stage 1: Intent Projection across 100 Capabilities\nMATCH (c:Capability)\nWHERE c.id IN ["cap_db_diagnostics", "cap_incident_alerting"]\n\n// Stage 2: Tool Isolation & Continual Weight Reweighting\nMATCH (t:Tool)-[:PROVIDES]->(c)\nOPTIONAL MATCH (c)-[p:PREFERS]->(t)\nWITH t, c, coalesce(p.weight, 1.0) AS relevance_weight\n\n// Stage 3: Multi-Hop Entity Resolution & Chaining\nOPTIONAL MATCH (t)-[r:REQUIRES_ENTITY|RESOLVES_ENTITY]->(e:Entity)\nRETURN t, c, e, relevance_weight\nORDER BY relevance_weight DESC\nLIMIT 2;`, "cypher1")}
                  className="absolute top-3 right-3 px-2 py-1 bg-white/10 hover:bg-white/20 text-gray-300 text-[10px] flex items-center gap-1 transition-colors"
                >
                  {copiedSnippet === "cypher1" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedSnippet === "cypher1" ? "COPIED" : "COPY"}</span>
                </button>
                <pre className="text-gray-200">
{`// Stage 1: Intent Projection across 100 Capabilities
MATCH (c:Capability)
WHERE c.id IN ["cap_db_diagnostics", "cap_incident_alerting"]

// Stage 2: Tool Isolation & Continual Weight Reweighting
MATCH (t:Tool)-[:PROVIDES]->(c)
OPTIONAL MATCH (c)-[p:PREFERS]->(t)
WITH t, c, coalesce(p.weight, 1.0) AS relevance_weight

// Stage 3: Multi-Hop Entity Resolution & Chaining
OPTIONAL MATCH (t)-[r:REQUIRES_ENTITY|RESOLVES_ENTITY]->(e:Entity)
RETURN t, c, e, relevance_weight
ORDER BY relevance_weight DESC
LIMIT 2;`}
                </pre>
              </div>
            </section>

            {/* 05 // CONTINUAL LEARNING */}
            <section id="continual" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                05 // CONTINUAL LEARNING MEMORY
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                Dynamic Edge Reweighting
              </h2>
              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                Standard prompt engineering requires human engineers to edit prompt templates when an agent misselects tools. Lucen instead treats the context graph as a reinforcement learning state:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-swiss-mono text-xs">
                <div className="p-4 bg-white swiss-border">
                  <div className="text-emerald-700 font-bold mb-1">EXECUTION REWARD (+0.15)</div>
                  <p className="text-[11px] text-[#1A1A1A]/80 font-sans">
                    When an agent completes a task successfully, an atomic feedback transaction reinforces the <code>(Capability)-[:PREFERS]-&gt;(Tool)</code> edge weight by +0.15 (clamped at 3.5).
                  </p>
                </div>
                <div className="p-4 bg-white swiss-border">
                  <div className="text-red-700 font-bold mb-1">EXECUTION PENALTY (-0.25)</div>
                  <p className="text-[11px] text-[#1A1A1A]/80 font-sans">
                    When a tool fails or throws unhandled exceptions, the preference weight decays by -0.25 (floor at 0.2), automatically surfacing alternative tools on subsequent episodes.
                  </p>
                </div>
              </div>

              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10">
                <div className="text-gray-500 mb-1">// Continual Learning API Call Specimen</div>
                <pre className="text-gray-200">
{`POST /api/feedback
{
  "tool_id": "tool_pg_check_connection_pool",
  "success": true,
  "task": "Postgres connection pool leak"
}

// Response:
{
  "status": "success",
  "reward": "+0.15",
  "updated_edges": [
    {"source": "cap_db_diagnostics", "target": "tool_pg_check_connection_pool", "new_weight": 2.55}
  ],
  "current_accuracy_pct": 93.8
}`}
                </pre>
              </div>
            </section>

            {/* 06 // DROP-IN GATEWAY */}
            <section id="gateway" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                06 // INTEGRATION ARCHITECTURE
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                Drop-In MCP Gateway Protocol
              </h2>
              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                Lucen is packaged as a drop-in proxy. Autonomous coding agents (like Claude Desktop or Cursor) do not require code changes: they simply point to the Lucen gateway URI.
              </p>

              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10 relative">
                <button
                  onClick={() => handleCopy(`{\n  "mcpServers": {\n    "lucen_gateway": {\n      "command": "python",\n      "args": ["-m", "backend.gateway", "--port", "8080"],\n      "env": {\n        "HYDRADB_ENDPOINT": "http://localhost:8080",\n        "S3_ENDPOINT": "http://localhost:9000"\n      }\n    }\n  }\n}`, "mcpcfg")}
                  className="absolute top-3 right-3 px-2 py-1 bg-white/10 hover:bg-white/20 text-gray-300 text-[10px] flex items-center gap-1 transition-colors"
                >
                  {copiedSnippet === "mcpcfg" ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedSnippet === "mcpcfg" ? "COPIED" : "COPY"}</span>
                </button>
                <div className="text-gray-500 mb-2">// Claude Desktop / Cursor Config (claude_desktop_config.json)</div>
                <pre className="text-gray-200">
{`{
  "mcpServers": {
    "lucen_gateway": {
      "command": "python",
      "args": ["-m", "backend.gateway", "--port", "8080"],
      "env": {
        "HYDRADB_ENDPOINT": "http://localhost:8080",
        "S3_ENDPOINT": "http://localhost:9000"
      }
    }
  }
}`}
                </pre>
              </div>

              <p className="text-xs text-[#1A1A1A]/80 font-sans">
                At runtime, when the agent invokes <code>tools/list</code>, Lucen intercepts the call, executes a 1.8ms GraphBLAS traversal against HydraDB based on the conversation turn, and mounts <strong>only the 2 to 4 required tools</strong> along with pre-resolved infrastructure credentials.
              </p>
            </section>

            {/* 07 // REST API REFERENCE */}
            <section id="api" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                07 // API REFERENCE
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                REST Service Endpoints
              </h2>
              <p className="text-sm text-[#1A1A1A]/85">
                The backend service runs on port 8000 and exposes full OpenAPI v3 documentation at <code>/docs</code>.
              </p>

              <div className="space-y-3 font-swiss-mono text-xs">
                <div className="p-4 bg-white swiss-border">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 bg-blue-100 text-[#0033A0] font-bold">POST</span>
                    <span className="font-bold">/api/traverse</span>
                  </div>
                  <p className="text-[11px] text-gray-600 font-sans mt-1">
                    Execute query-time GraphBLAS traversal. Accepts <code>task</code> prompt and optional <code>top_k_tools</code>. Returns isolated tools, bound entities, and token reduction economics.
                  </p>
                </div>

                <div className="p-4 bg-white swiss-border">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 bg-blue-100 text-[#0033A0] font-bold">POST</span>
                    <span className="font-bold">/api/feedback</span>
                  </div>
                  <p className="text-[11px] text-gray-600 font-sans mt-1">
                    Record execution reward or penalty for continual learning. Incrementally adjusts PREFERS edge weights.
                  </p>
                </div>

                <div className="p-4 bg-white swiss-border">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold">GET</span>
                    <span className="font-bold">/api/graph/stats</span>
                  </div>
                  <p className="text-[11px] text-gray-600 font-sans mt-1">
                    Retrieve live graph topology counts (50 servers, 500 tools, 100 capabilities, 80 entities, 2,421 edges).
                  </p>
                </div>

                <div className="p-4 bg-white swiss-border">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold">GET</span>
                    <span className="font-bold">/api/benchmark</span>
                  </div>
                  <p className="text-[11px] text-gray-600 font-sans mt-1">
                    Fetch standardized 5-scenario benchmark comparison between Naive Preload and Lucen GraphBLAS.
                  </p>
                </div>
              </div>
            </section>

            {/* 08 // CLI REFERENCE */}
            <section id="cli" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                08 // CLI REFERENCE
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                Command-Line Interface (`lucen.py`)
              </h2>
              <p className="text-sm text-[#1A1A1A]/85">
                The standalone CLI provides full parity with the web application and operates with zero browser dependency:
              </p>

              <div className="overflow-x-auto swiss-border font-swiss-mono text-xs">
                <table className="w-full text-left border-collapse">
                  <thead className="bg-[#F2F2F2] border-b border-[#1A1A1A]">
                    <tr>
                      <th className="p-3 font-bold">Command</th>
                      <th className="p-3 font-bold">Arguments</th>
                      <th className="p-3 font-bold">Description</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E2E6E6]">
                    <tr>
                      <td className="p-3 font-bold text-[#D82C2C]">stats</td>
                      <td className="p-3 text-gray-500">[--json]</td>
                      <td className="p-3">Prints graph topology counts and current continual learning accuracy.</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-bold text-[#D82C2C]">traverse</td>
                      <td className="p-3 text-gray-500">&lt;task_prompt&gt; [--top-k N]</td>
                      <td className="p-3">Executes GraphBLAS traversal and prints isolated tools and pre-bound entities.</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-bold text-[#D82C2C]">verify</td>
                      <td className="p-3 text-gray-500">None</td>
                      <td className="p-3">Runs automated 5-step engine parity test suite (topology, reduction, latency, learning, entities).</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-bold text-[#D82C2C]">feedback</td>
                      <td className="p-3 text-gray-500">--tool &lt;id&gt; [--reward|--penalty]</td>
                      <td className="p-3">Simulates atomic PREFERS edge weight updates in HydraDB continual learning memory.</td>
                    </tr>
                    <tr>
                      <td className="p-3 font-bold text-[#D82C2C]">serve</td>
                      <td className="p-3 text-gray-500">[--port 8000]</td>
                      <td className="p-3">Starts the FastAPI backend service daemon on designated host and port.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>

            {/* 09 // BENCHMARKS METHODOLOGY */}
            <section id="benchmarks" className="space-y-5 scroll-mt-24 pt-8 border-t border-[#E2E6E6]">
              <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
                09 // BENCHMARK METHODOLOGY
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-swiss-display text-[#1A1A1A]">
                Reproducible Evaluation Suite
              </h2>
              <p className="text-sm text-[#1A1A1A]/85 leading-relaxed">
                All benchmark numbers published in the documentation and research publication are 100% reproducible by running the automated benchmark suite:
              </p>

              <div className="bg-[#0E1117] text-white p-4 font-swiss-mono text-xs border border-white/10">
                <pre className="text-gray-200">
{`# Execute 50-task empirical evaluation across Naive, Vector Top-K, and Lucen
python eval/benchmark_eval.py

# Execute full 9-part live integration test suite
python eval/live_e2e_test.py`}
                </pre>
              </div>

              <div className="p-4 bg-[#F2F2F2] swiss-border text-xs font-swiss-mono space-y-1">
                <div className="font-bold text-[#1A1A1A]">METRIC RIGOR GUARANTEE:</div>
                <div className="text-gray-600 font-sans">
                  Zero simulated vanity numbers. The 50-task dataset uses strict held-out testing (35 train / 15 test). Tool recall requires exact parameter matching, and entity resolution checks live connection parity.
                </div>
              </div>
            </section>

          </main>
        </div>
      </div>
    </div>
  );
}
