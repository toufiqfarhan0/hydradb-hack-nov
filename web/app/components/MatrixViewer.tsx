"use client";

import React, { useState, useRef } from "react";
import { Move, RotateCcw } from "lucide-react";

export interface GraphNode {
  id: string;
  label: string;
  type: "MCPServer" | "Capability" | "Tool" | "Entity";
  x: number;
  y: number;
  active: boolean;
}

const DEFAULT_NODES: GraphNode[] = [
  // Tier 1: MCP Servers (x = 160)
  { id: "s1", label: "PostgreSQL Inspector", type: "MCPServer", x: 160, y: 120, active: true },
  { id: "s2", label: "Slack Enterprise", type: "MCPServer", x: 160, y: 220, active: true },
  { id: "s3", label: "GitHub Repo Mgr", type: "MCPServer", x: 160, y: 320, active: false },
  { id: "s4", label: "AWS Cloud Ops", type: "MCPServer", x: 160, y: 420, active: false },

  // Tier 2: Capabilities (x = 440)
  { id: "c1", label: "Database Diagnostics", type: "Capability", x: 440, y: 160, active: true },
  { id: "c2", label: "Incident Alerting", type: "Capability", x: 440, y: 270, active: true },
  { id: "c3", label: "Code Review & PR", type: "Capability", x: 440, y: 380, active: false },

  // Tier 3: Tools (x = 730)
  { id: "t1", label: "pg_check_connection_pool", type: "Tool", x: 710, y: 150, active: true },
  { id: "t2", label: "slack_post_incident_bulletin", type: "Tool", x: 750, y: 240, active: true },
  { id: "t3", label: "docker_restart_container", type: "Tool", x: 710, y: 330, active: false },
  { id: "t4", label: "aws_fetch_rds_metrics", type: "Tool", x: 750, y: 410, active: false },

  // Tier 4: Entities (x = 970)
  { id: "e1", label: "Production DB Primary", type: "Entity", x: 970, y: 160, active: true },
  { id: "e2", label: "Slack #incident-critical-ops", type: "Entity", x: 970, y: 260, active: true },
  { id: "e3", label: "GitHub PR #842", type: "Entity", x: 970, y: 370, active: false }
];

export default function MatrixViewer() {
  const [nodes, setNodes] = useState<GraphNode[]>(DEFAULT_NODES);
  const [graphFilter, setGraphFilter] = useState<"all" | "active">("all");
  const [draggedNodeId, setDraggedNodeId] = useState<string | null>(null);
  const dragOffsetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const svgRef = useRef<SVGSVGElement | null>(null);

  const handlePointerDown = (id: string, e: React.PointerEvent) => {
    e.preventDefault();
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    const scaleX = 1100 / rect.width;
    const scaleY = 520 / rect.height;
    const clickX = (e.clientX - rect.left) * scaleX;
    const clickY = (e.clientY - rect.top) * scaleY;

    const node = nodes.find((n) => n.id === id);
    if (!node) return;

    dragOffsetRef.current = { x: clickX - node.x, y: clickY - node.y };
    setDraggedNodeId(id);
    (e.target as Element).setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e: React.PointerEvent) => {
    if (!draggedNodeId) return;
    const svg = svgRef.current;
    if (!svg) return;
    const rect = svg.getBoundingClientRect();
    const scaleX = 1100 / rect.width;
    const scaleY = 520 / rect.height;
    const currentX = (e.clientX - rect.left) * scaleX;
    const currentY = (e.clientY - rect.top) * scaleY;

    const newX = Math.max(40, Math.min(1060, currentX - dragOffsetRef.current.x));
    const newY = Math.max(40, Math.min(480, currentY - dragOffsetRef.current.y));

    setNodes((prev) =>
      prev.map((n) => (n.id === draggedNodeId ? { ...n, x: newX, y: newY } : n))
    );
  };

  const handlePointerUp = (e: React.PointerEvent) => {
    if (draggedNodeId) {
      try {
        (e.target as Element).releasePointerCapture(e.pointerId);
      } catch {
        // Safe fallback
      }
      setDraggedNodeId(null);
    }
  };

  const handleReset = () => {
    setNodes(DEFAULT_NODES);
  };

  const nodeMap = new Map<string, GraphNode>();
  nodes.forEach((n) => nodeMap.set(n.id, n));

  const activeEdges: [string, string][] = [
    ["s1", "c1"],
    ["s2", "c2"],
    ["c1", "t1"],
    ["c2", "t2"],
    ["t1", "e1"],
    ["t2", "e2"]
  ];

  const inactiveEdges: [string, string][] = [
    ["s3", "c3"],
    ["s4", "c3"],
    ["c3", "t3"],
    ["c3", "t4"],
    ["t3", "e3"],
    ["t4", "e3"]
  ];

  const lanes = [
    { title: "TIER 1 // MCP SERVERS (50)", x: 160, color: "#60A5FA" },
    { title: "TIER 2 // CAPABILITIES (100)", x: 440, color: "#FBBF24" },
    { title: "TIER 3 // TOOLS (500)", x: 730, color: "#EF4444" },
    { title: "TIER 4 // BOUND ENTITIES (80)", x: 970, color: "#34D399" }
  ];

  return (
    <div className="bg-white p-6 swiss-border space-y-4">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-swiss-mono text-[#D82C2C] uppercase font-bold tracking-wider">
            GRAPH TOPOLOGY VIEWER
          </div>
          <h2 className="text-2xl font-bold tracking-tight font-swiss-display text-[#1A1A1A] mt-1">
            Interactive GraphBLAS Matrix Canvas
          </h2>
          <p className="text-xs font-swiss-mono text-[#A9B2B1] mt-1 flex items-center gap-1.5">
            <Move className="w-3.5 h-3.5 text-[#D82C2C]" />
            <span>Click and drag any node or label to reposition. Connections redraw in real-time.</span>
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setGraphFilter("all")}
            className={`px-3 py-1.5 text-xs font-swiss-mono border transition-colors cursor-pointer ${
              graphFilter === "all"
                ? "bg-[#1A1A1A] text-white border-[#1A1A1A] font-bold"
                : "bg-[#F2F2F2] border-[#E2E6E6] text-[#1A1A1A]"
            }`}
          >
            All Nodes
          </button>
          <button
            onClick={() => setGraphFilter("active")}
            className={`px-3 py-1.5 text-xs font-swiss-mono border transition-colors cursor-pointer ${
              graphFilter === "active"
                ? "bg-[#D82C2C] text-white border-[#D82C2C] font-bold"
                : "bg-[#F2F2F2] border-[#E2E6E6] text-[#1A1A1A]"
            }`}
          >
            Active Path Only
          </button>
          <button
            onClick={handleReset}
            className="px-3 py-1.5 text-xs font-swiss-mono border border-[#E2E6E6] bg-[#F2F2F2] hover:bg-white text-[#1A1A1A] transition-colors flex items-center gap-1.5 cursor-pointer"
            title="Reset nodes to default lane positions"
          >
            <RotateCcw className="w-3 h-3 text-[#D82C2C]" />
            <span>Reset Layout</span>
          </button>
        </div>
      </div>

      <div className="bg-[#0E1117] border border-[#23272F] overflow-hidden shadow-sm">
        {/* Telemetry Header */}
        <div className="flex items-center justify-between p-3.5 bg-[#161B22] border-b border-[#23272F] text-xs font-swiss-mono">
          <div className="flex items-center gap-4 text-gray-300">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-[#60A5FA]" /> MCP Servers
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-[#FBBF24]" /> Capabilities
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-[#EF4444]" /> Tools
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-[#34D399]" /> Entities
            </span>
          </div>
          <span className="text-emerald-400 font-bold tracking-wider">
            730 NODES · 2,421 EDGES · 1.8ms LATENCY
          </span>
        </div>

        {/* SVG Canvas */}
        <div className="w-full relative select-none bg-[#0E1117]">
          <svg
            ref={svgRef}
            viewBox="0 0 1100 520"
            className="w-full h-auto block select-none cursor-default bg-[#0E1117]"
            onPointerMove={handlePointerMove}
            onPointerUp={handlePointerUp}
          >
            <defs>
              <filter id="glow-red" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor="#D82C2C" floodOpacity="0.8" />
              </filter>
              <filter id="glow-node" x="-30%" y="-30%" width="160%" height="160%">
                <feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#FFFFFF" floodOpacity="0.5" />
              </filter>
              <pattern id="grid-dots" width="40" height="40" patternUnits="userSpaceOnUse">
                <circle cx="2" cy="2" r="1" fill="rgba(255,255,255,0.06)" />
              </pattern>
            </defs>

            {/* Background pattern */}
            <rect width="1100" height="520" fill="#0E1117" />
            <rect width="1100" height="520" fill="url(#grid-dots)" />

            {/* 4 Swimlanes */}
            {lanes.map((lane) => (
              <g key={lane.title}>
                <line
                  x1={lane.x}
                  y1={35}
                  x2={lane.x}
                  y2={500}
                  stroke="rgba(255, 255, 255, 0.12)"
                  strokeDasharray="4 6"
                />
                <text
                  x={lane.x}
                  y={24}
                  fill={lane.color}
                  fontSize="9.5"
                  fontWeight="bold"
                  fontFamily="'JetBrains Mono', monospace"
                  textAnchor="middle"
                >
                  {lane.title}
                </text>
              </g>
            ))}

            {/* Inactive Edges */}
            {graphFilter === "all" &&
              inactiveEdges.map(([sId, tId]) => {
                const s = nodeMap.get(sId);
                const t = nodeMap.get(tId);
                if (!s || !t) return null;
                return (
                  <line
                    key={`inact-${sId}-${tId}`}
                    x1={s.x}
                    y1={s.y}
                    x2={t.x}
                    y2={t.y}
                    stroke="rgba(255, 255, 255, 0.14)"
                    strokeWidth="1.2"
                    strokeDasharray="3 3"
                  />
                );
              })}

            {/* Active Edges */}
            {activeEdges.map(([sId, tId]) => {
              const s = nodeMap.get(sId);
              const t = nodeMap.get(tId);
              if (!s || !t) return null;
              if (graphFilter === "active" && (!s.active || !t.active)) return null;

              const dx = t.x - s.x;
              const cp1x = s.x + dx * 0.45;
              const cp2x = s.x + dx * 0.55;
              const pathD = `M ${s.x} ${s.y} C ${cp1x} ${s.y}, ${cp2x} ${t.y}, ${t.x} ${t.y}`;

              return (
                <g key={`act-${sId}-${tId}`}>
                  <path
                    d={pathD}
                    fill="none"
                    stroke="#D82C2C"
                    strokeWidth="4"
                    opacity="0.25"
                  />
                  <path
                    d={pathD}
                    fill="none"
                    stroke="#D82C2C"
                    strokeWidth="2.2"
                    filter="url(#glow-red)"
                  />
                </g>
              );
            })}

            {/* Nodes */}
            {nodes.map((node) => {
              if (graphFilter === "active" && !node.active) return null;
              const isDragged = draggedNodeId === node.id;

              let pillAnchor: "start" | "middle" | "end" = "middle";
              let pillX = node.x;
              let pillY = node.y - 18;

              if (node.type === "MCPServer") {
                pillAnchor = "end";
                pillX = node.x - 16;
                pillY = node.y + 4;
              } else if (node.type === "Entity") {
                pillAnchor = "start";
                pillX = node.x + 16;
                pillY = node.y + 4;
              } else if (node.type === "Tool") {
                pillAnchor = node.x < 730 ? "end" : "start";
                pillX = node.x < 730 ? node.x - 14 : node.x + 14;
                pillY = node.y + 4;
              }

              const pillWidth = node.label.length * 6.8 + 14;
              const pillBoxX =
                pillAnchor === "middle"
                  ? pillX - pillWidth / 2
                  : pillAnchor === "end"
                  ? pillX - pillWidth
                  : pillX;

              return (
                <g
                  key={node.id}
                  className="cursor-grab active:cursor-grabbing transition-transform"
                  onPointerDown={(e) => handlePointerDown(node.id, e)}
                >
                  {/* Outer glow ring when dragged */}
                  {isDragged && (
                    <circle
                      cx={node.x}
                      cy={node.y}
                      r="22"
                      fill="rgba(216, 44, 44, 0.3)"
                      stroke="#D82C2C"
                      strokeWidth="1.5"
                    />
                  )}

                  {/* Node Circle */}
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={isDragged ? 12 : node.active ? 9.5 : 7.5}
                    fill={node.active ? "#FFFFFF" : "#374151"}
                    stroke={
                      isDragged
                        ? "#FFFFFF"
                        : node.active
                        ? "#D82C2C"
                        : "rgba(255, 255, 255, 0.25)"
                    }
                    strokeWidth={isDragged ? 3 : node.active ? 2.5 : 1}
                    filter={node.active ? "url(#glow-node)" : undefined}
                  />

                  {/* Label Pill Box */}
                  <rect
                    x={pillBoxX}
                    y={pillY - 12}
                    width={pillWidth}
                    height="19"
                    rx="2"
                    fill={
                      isDragged
                        ? "#D82C2C"
                        : node.active
                        ? "rgba(216, 44, 44, 0.95)"
                        : "rgba(15, 23, 42, 0.88)"
                    }
                    stroke={
                      isDragged
                        ? "#FFFFFF"
                        : node.active
                        ? "#FFFFFF"
                        : "rgba(255, 255, 255, 0.18)"
                    }
                    strokeWidth={isDragged ? 1.8 : 1}
                  />

                  {/* Label Text */}
                  <text
                    x={pillAnchor === "middle" ? pillX : pillAnchor === "end" ? pillX - 6 : pillX + 6}
                    y={pillY + 2}
                    fill={node.active || isDragged ? "#FFFFFF" : "#9CA3AF"}
                    fontSize={node.active ? "9.5" : "8.5"}
                    fontWeight={node.active ? "bold" : "normal"}
                    fontFamily="'JetBrains Mono', monospace"
                    textAnchor={pillAnchor}
                  >
                    {node.label}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Lane Footer Legend */}
        <div className="grid grid-cols-4 bg-[#161B22] border-t border-[#23272F] p-3 text-[11px] font-swiss-mono text-center text-gray-400">
          <div>TIER 1: MCP SERVERS</div>
          <div>TIER 2: CAPABILITY RESOLVERS</div>
          <div>TIER 3: ISOLATED VS PRUNED TOOLS</div>
          <div>TIER 4: BOUND ENTITIES</div>
        </div>
      </div>
    </div>
  );
}
