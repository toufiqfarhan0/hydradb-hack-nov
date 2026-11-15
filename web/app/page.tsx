"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import Navbar from "./components/Navbar";
import {
  Play,
  Terminal,
  Cpu,
  Database,
  CheckCircle2,
  Copy,
  Check,
  RefreshCw,
  Layers,
  ShieldCheck,
  Zap,
  ArrowRight,
  Sliders,
  AlertCircle,
  Move,
  RotateCcw
} from "lucide-react";

interface ToolItem {
  name: string;
  server: string;
  cost: number;
  desc: string;
}

interface EntityItem {
  name: string;
  type: string;
  props: Record<string, any>;
}

interface PresetItem {
  id: string;
  label: string;
  task: string;
  tools: ToolItem[];
  entities: EntityItem[];
  tokens: number;
  reduction: number;
}

const PRESETS: PresetItem[] = [
  {
    id: "p0_postgres",
    label: "P0 Outage: Postgres Leak",
    task: "Production Postgres DB is exhausting connections and throwing 500s. Inspect pool and broadcast alert to Slack war room.",
    tools: [
      { name: "pg_check_connection_pool", server: "mcp_postgres", cost: 380, desc: "Queries PgBouncer and pool utilization metrics" },
      { name: "slack_post_incident_bulletin", server: "mcp_slack", cost: 480, desc: "Broadcasts structured alert to targeted war-room channel" }
    ],
    entities: [
      { name: "Production DB Primary & Read Replica", type: "DatabaseCluster", props: { host: "pg-cluster-prod.internal:5432", max_conns: 400, current: 387 } },
      { name: "Slack #incident-critical-ops", type: "SlackChannel", props: { channel_id: "C08A91KL2", tier: "P0" } }
    ],
    tokens: 1140,
    reduction: 93.8
  },
  {
    id: "devops_docker",
    label: "DevOps: OOM Restart",
    task: "Docker worker container 'hydra-worker-api-4' is OOM killed. Inspect stderr logs and execute rolling container restart.",
    tools: [
      { name: "docker_stream_container_logs", server: "mcp_docker", cost: 440, desc: "Streams stderr/stdout tail for crashing container" },
      { name: "docker_restart_container_instance", server: "mcp_docker", cost: 520, desc: "Triggers graceful rolling restart" }
    ],
    entities: [
      { name: "Docker Container 'hydra-worker-api-4'", type: "ContainerInstance", props: { container_id: "a918f0cb18a2", status: "unhealthy (OOM)" } }
    ],
    tokens: 1210,
    reduction: 93.4
  },
  {
    id: "pagerduty_alert",
    label: "Incident Alerting",
    task: "High severity crash spike detected. Page on-call infrastructure lead and publish bulletin in #incident-critical-ops.",
    tools: [
      { name: "slack_page_oncall_engineer", server: "mcp_slack", cost: 410, desc: "Triggers emergency alert with priority override" },
      { name: "slack_post_incident_bulletin", server: "mcp_slack", cost: 480, desc: "Publishes live bulletin with threaded resolution status" }
    ],
    entities: [
      { name: "Slack #incident-critical-ops", type: "SlackChannel", props: { channel_id: "C08A91KL2", tier: "P0" } }
    ],
    tokens: 980,
    reduction: 94.7
  },
  {
    id: "github_pr",
    label: "Hotfix PR Review",
    task: "Review git diff for hotfix PR #842 and merge to main branch after verifying CI checks pass.",
    tools: [
      { name: "github_inspect_commit_diff", server: "mcp_github", cost: 460, desc: "Fetches unified diff for specific pull request" },
      { name: "github_create_pull_request", server: "mcp_github", cost: 510, desc: "Automates branch creation, commits, and PR reviews" }
    ],
    entities: [
      { name: "GitHub PR #842 (Fix pool leak)", type: "PullRequest", props: { repo: "hydra-corp/core-api", branch: "fix/db-pool-exhaustion" } }
    ],
    tokens: 1380,
    reduction: 92.5
  },
  {
    id: "aws_rds",
    label: "AWS RDS CloudWatch",
    task: "Fetch last 60 minutes CloudWatch metrics for AWS RDS instance and evaluate CPU utilization and memory pressure.",
    tools: [
      { name: "aws_fetch_rds_metrics", server: "mcp_aws", cost: 490, desc: "Retrieves CPU, ReadIOPS, and FreeableMemory CloudWatch metrics" },
      { name: "aws_restart_ecs_service", server: "mcp_aws", cost: 530, desc: "Triggers rolling ECS service task update" }
    ],
    entities: [
      { name: "AWS RDS 'hydra-aurora-prod'", type: "CloudResource", props: { arn: "arn:aws:rds:us-east-1:991283:hydra-aurora-prod" } }
    ],
    tokens: 1040,
    reduction: 94.4
  }
];

const BENCHMARKS = [
  { task_name: "Outage Triage: Postgres Connection Exhaustion", domain: "Database Infrastructure", naive_tokens: 18450, lucen_tokens: 1140, reduction_pct: 93.8, naive_lat: 1840, lucen_lat: 115, accuracy_gain: 26.4 },
  { task_name: "DevOps: Rolling Container Restart on OOM Alert", domain: "Container Runtime", naive_tokens: 18450, lucen_tokens: 1210, reduction_pct: 93.4, naive_lat: 1720, lucen_lat: 98, accuracy_gain: 31.2 },
  { task_name: "Incident Response: PagerDuty Page & War-Room Bulletin", domain: "Collaboration", naive_tokens: 18450, lucen_tokens: 980, reduction_pct: 94.7, naive_lat: 1610, lucen_lat: 86, accuracy_gain: 19.8 },
  { task_name: "Hotfix PR Review & Diff Verification", domain: "Software Engineering", naive_tokens: 18450, lucen_tokens: 1380, reduction_pct: 92.5, naive_lat: 1950, lucen_lat: 124, accuracy_gain: 24.5 },
  { task_name: "Cloud Cost & RDS Provisioned IOPS Metrics", domain: "Cloud Operations", naive_tokens: 18450, lucen_tokens: 1040, reduction_pct: 94.4, naive_lat: 1680, lucen_lat: 92, accuracy_gain: 28.1 }
];

export default function Home() {
  const [selectedPreset, setSelectedPreset] = useState<number>(0);
  const [taskPrompt, setTaskPrompt] = useState<string>(PRESETS[0].task);
  const [isTraversing, setIsTraversing] = useState<boolean>(false);
  const [traversalResult, setTraversalResult] = useState<PresetItem>(PRESETS[0]);
  const [copiedCypher, setCopiedCypher] = useState<boolean>(false);

  // Continual Learning State
  const [accuracy, setAccuracy] = useState<number>(98.4);
  const [feedbackLog, setFeedbackLog] = useState<string[]>([
    "System ready. Select a feedback action above to witness dynamic HydraDB weight adjustment."
  ]);

  // Topology Visualizer State & Interactive Drag Engine
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [graphFilter, setGraphFilter] = useState<"all" | "active">("all");
  const nodesRef = useRef<any[]>([]);
  const draggedNodeIdxRef = useRef<number | null>(null);
  const dragOffsetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  // FAQ Accordion State
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  // CLI Simulator State
  const [selectedCliTab, setSelectedCliTab] = useState<number>(0);
  const [copiedCli, setCopiedCli] = useState<boolean>(false);

  const handleSelectPreset = (idx: number) => {
    setSelectedPreset(idx);
    const p = PRESETS[idx];
    setTaskPrompt(p.task);
    setTraversalResult(p);
  };

  const handleExecuteTraversal = async () => {
    setIsTraversing(true);
    try {
      const res = await fetch("/api/traverse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: taskPrompt, mode: "lucen_graph" })
      });
      if (res.ok) {
        const data = await res.json();
        setTraversalResult({
          id: "custom",
          label: "Custom Query",
          task: data.task,
          tools: data.selected_tools.map((t: any) => ({
            name: t.name,
            server: t.server_id,
            cost: t.estimated_token_cost,
            desc: t.description
          })),
          entities: data.resolved_entities.map((e: any) => ({
            name: e.name,
            type: e.entity_type,
            props: e.properties
          })),
          tokens: data.tokens_used,
          reduction: data.token_reduction_pct
        });
      } else {
        fallbackClientTraversal();
      }
    } catch {
      fallbackClientTraversal();
    } finally {
      setIsTraversing(false);
    }
  };

  const fallbackClientTraversal = () => {
    const matched = PRESETS.find(p =>
      taskPrompt.toLowerCase().includes(p.id.split("_")[1])
    ) || PRESETS[selectedPreset];
    setTraversalResult(matched);
  };

  const handleSimulateFeedback = (success: boolean) => {
    const delta = success ? 0.8 : -1.2;
    const newAcc = Math.min(Math.max(Number((accuracy + delta).toFixed(1)), 70.0), 99.4);
    setAccuracy(newAcc);

    const toolName = traversalResult.tools[0]?.name || "pg_check_connection_pool";
    const time = new Date().toLocaleTimeString();
    const entry = success
      ? `[REWARD +0.15] ${time}: Reinforced (:Capability)-[:PREFERS]->(${toolName}). Accuracy: ${newAcc}%`
      : `[PENALTY -0.25] ${time}: Decayed (:Capability)-[:PREFERS]->(${toolName}). Accuracy: ${newAcc}%`;

    setFeedbackLog(prev => [entry, ...prev.slice(0, 4)]);
  };

  const copyCypher = () => {
    const query = `MATCH (c:Capability) WHERE c.id IN ["cap_db_diagnostics", "cap_incident_alerting"]\nMATCH (t:Tool)-[:PROVIDES]->(c)\nOPTIONAL MATCH (c)-[p:PREFERS]->(t)\nWITH t, c, coalesce(p.weight, 1.0) AS relevance_weight\nOPTIONAL MATCH (t)-[r:REQUIRES_ENTITY|RESOLVES_ENTITY]->(e:Entity)\nRETURN t, c, e, relevance_weight\nORDER BY relevance_weight DESC\nLIMIT 2;`;
    navigator.clipboard.writeText(query);
    setCopiedCypher(true);
    setTimeout(() => setCopiedCypher(false), 2000);
  };

  const getInitialNodes = (w: number) => [
    { id: "s1", label: "PostgreSQL Inspector", type: "MCPServer", x: w * 0.14, y: 120, active: true },
    { id: "s2", label: "Slack Enterprise", type: "MCPServer", x: w * 0.14, y: 220, active: true },
    { id: "s3", label: "GitHub Repo Mgr", type: "MCPServer", x: w * 0.14, y: 320, active: false },
    { id: "s4", label: "AWS Cloud Ops", type: "MCPServer", x: w * 0.14, y: 420, active: false },

    { id: "c1", label: "Database Diagnostics", type: "Capability", x: w * 0.38, y: 160, active: true },
    { id: "c2", label: "Incident Alerting", type: "Capability", x: w * 0.38, y: 270, active: true },
    { id: "c3", label: "Code Review & PR", type: "Capability", x: w * 0.38, y: 380, active: false },

    { id: "t1", label: "pg_check_connection_pool", type: "Tool", x: w * 0.65 - 18, y: 150, active: true },
    { id: "t2", label: "slack_post_incident_bulletin", type: "Tool", x: w * 0.65 + 18, y: 240, active: true },
    { id: "t3", label: "docker_restart_container", type: "Tool", x: w * 0.65 - 18, y: 330, active: false },
    { id: "t4", label: "aws_fetch_rds_metrics", type: "Tool", x: w * 0.65 + 18, y: 410, active: false },

    { id: "e1", label: "Production DB Primary", type: "Entity", x: w * 0.88, y: 160, active: true },
    { id: "e2", label: "Slack #incident-critical-ops", type: "Entity", x: w * 0.88, y: 260, active: true },
    { id: "e3", label: "GitHub PR #842", type: "Entity", x: w * 0.88, y: 370, active: false }
  ];

  const drawTopology = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    // 4 Vertical Lanes
    const lanes = [
      { name: "TIER 1 // MCP SERVERS (8)", x: w * 0.14, color: "#60A5FA" },
      { name: "TIER 2 // CAPABILITIES (10)", x: w * 0.38, color: "#FBBF24" },
      { name: "TIER 3 // TOOLS (19)", x: w * 0.65, color: "#EF4444" },
      { name: "TIER 4 // BOUND ENTITIES (7)", x: w * 0.88, color: "#34D399" }
    ];

    lanes.forEach(lane => {
      ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
      ctx.setLineDash([4, 6]);
      ctx.beginPath();
      ctx.moveTo(lane.x, 35);
      ctx.lineTo(lane.x, h - 20);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.font = "bold 9.5px 'JetBrains Mono', monospace";
      ctx.fillStyle = lane.color;
      ctx.textAlign = "center";
      ctx.fillText(lane.name, lane.x, 26);
    });

    const nodes = nodesRef.current;
    if (!nodes || nodes.length === 0) return;

    // Draw Inactive Background Edges
    const inactiveEdges: [number, number][] = [
      [2, 6], [3, 6], [6, 9], [6, 10], [9, 13], [10, 13]
    ];
    if (graphFilter === "all") {
      inactiveEdges.forEach(([sIdx, tIdx]) => {
        const s = nodes[sIdx];
        const t = nodes[tIdx];
        if (!s || !t) return;
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(t.x, t.y);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
        ctx.lineWidth = 1;
        ctx.stroke();
      });
    }

    // Draw Active Edges
    const activeEdges: [number, number][] = [
      [0, 4], [1, 5], [4, 7], [5, 8], [7, 11], [8, 12]
    ];
    activeEdges.forEach(([sIdx, tIdx]) => {
      const s = nodes[sIdx];
      const t = nodes[tIdx];
      if (!s || !t) return;
      if (graphFilter === "active" && (!s.active || !t.active)) return;

      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(t.x, t.y);
      ctx.strokeStyle = "#D82C2C";
      ctx.lineWidth = 2.5;
      ctx.stroke();
    });

    // Draw Nodes
    nodes.forEach((n, idx) => {
      if (graphFilter === "active" && !n.active) return;
      const isDragged = draggedNodeIdxRef.current === idx;

      // Glow ring when dragging
      if (isDragged) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, 22, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(216, 44, 44, 0.25)";
        ctx.fill();
      }

      ctx.beginPath();
      ctx.arc(n.x, n.y, isDragged ? 13 : (n.active ? 10 : 8), 0, Math.PI * 2);
      ctx.fillStyle = n.active ? "#FFFFFF" : "#4B5563";
      ctx.fill();

      ctx.lineWidth = isDragged ? 3.5 : (n.active ? 2.5 : 1);
      ctx.strokeStyle = isDragged ? "#FFFFFF" : (n.active ? "#D82C2C" : "rgba(255, 255, 255, 0.2)");
      ctx.stroke();

      // Label with pill backdrop
      ctx.font = n.active ? "bold 9.5px 'JetBrains Mono', monospace" : "8.5px 'JetBrains Mono', monospace";
      const metrics = ctx.measureText(n.label);
      const bw = metrics.width + 12;
      const bh = 18;
      let lx = n.x;
      let ly = n.y;
      let align: CanvasTextAlign = "center";

      if (n.type === "MCPServer") {
        lx = n.x - 16;
        ly = n.y + 4;
        align = "right";
      } else if (n.type === "Entity") {
        lx = n.x + 16;
        ly = n.y + 4;
        align = "left";
      } else if (n.type === "Tool") {
        lx = n.x < w * 0.65 ? n.x - 14 : n.x + 14;
        ly = n.y + 4;
        align = n.x < w * 0.65 ? "right" : "left";
      } else {
        lx = n.x;
        ly = n.y - 14;
        align = "center";
      }

      ctx.save();
      let rx = lx;
      if (align === "center") rx = lx - bw / 2;
      else if (align === "right") rx = lx - bw;

      // Save hit box for collision detection
      n.bbox = { x: rx, y: ly - 12, w: bw, h: bh };

      ctx.fillStyle = isDragged
        ? "#D82C2C"
        : n.active
        ? "rgba(216, 44, 44, 0.95)"
        : "rgba(15, 23, 42, 0.85)";
      ctx.strokeStyle = isDragged ? "#FFFFFF" : (n.active ? "#FFFFFF" : "rgba(255, 255, 255, 0.15)");
      ctx.lineWidth = isDragged ? 2 : 1;
      ctx.fillRect(rx, ly - 12, bw, bh);
      ctx.strokeRect(rx, ly - 12, bw, bh);

      ctx.fillStyle = n.active || isDragged ? "#FFFFFF" : "#C9D1D9";
      ctx.textAlign = align;
      ctx.fillText(n.label, lx, ly);
      ctx.restore();
    });
  };

  const getCanvasCoords = (e: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    let clientX = 0;
    let clientY = 0;
    if ("touches" in e) {
      if (e.touches && e.touches.length > 0) {
        clientX = e.touches[0].clientX;
        clientY = e.touches[0].clientY;
      }
    } else {
      clientX = e.clientX;
      clientY = e.clientY;
    }
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const { x, y } = getCanvasCoords(e);
    const nodes = nodesRef.current;
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      if (graphFilter === "active" && !n.active) continue;
      const dist = Math.hypot(x - n.x, y - n.y);
      const inBox = n.bbox && x >= n.bbox.x && x <= n.bbox.x + n.bbox.w && y >= n.bbox.y && y <= n.bbox.y + n.bbox.h;
      if (dist <= 20 || inBox) {
        draggedNodeIdxRef.current = i;
        dragOffsetRef.current = { x: x - n.x, y: y - n.y };
        if (canvasRef.current) canvasRef.current.style.cursor = "grabbing";
        drawTopology();
        break;
      }
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const { x, y } = getCanvasCoords(e);
    const canvas = canvasRef.current;
    if (!canvas) return;

    if (draggedNodeIdxRef.current !== null) {
      const idx = draggedNodeIdxRef.current;
      const n = nodesRef.current[idx];
      if (n) {
        n.x = Math.max(30, Math.min(canvas.width - 30, x - dragOffsetRef.current.x));
        n.y = Math.max(30, Math.min(canvas.height - 30, y - dragOffsetRef.current.y));
        drawTopology();
      }
    } else {
      const nodes = nodesRef.current;
      let hovered = false;
      for (let i = 0; i < nodes.length; i++) {
        const n = nodes[i];
        if (graphFilter === "active" && !n.active) continue;
        const dist = Math.hypot(x - n.x, y - n.y);
        const inBox = n.bbox && x >= n.bbox.x && x <= n.bbox.x + n.bbox.w && y >= n.bbox.y && y <= n.bbox.y + n.bbox.h;
        if (dist <= 20 || inBox) {
          hovered = true;
          break;
        }
      }
      canvas.style.cursor = hovered ? "grab" : "default";
    }
  };

  const handleMouseUp = () => {
    draggedNodeIdxRef.current = null;
    if (canvasRef.current) canvasRef.current.style.cursor = "default";
    drawTopology();
  };

  const handleTouchStart = (e: React.TouchEvent<HTMLCanvasElement>) => {
    const { x, y } = getCanvasCoords(e);
    const nodes = nodesRef.current;
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      if (graphFilter === "active" && !n.active) continue;
      const dist = Math.hypot(x - n.x, y - n.y);
      const inBox = n.bbox && x >= n.bbox.x && x <= n.bbox.x + n.bbox.w && y >= n.bbox.y && y <= n.bbox.y + n.bbox.h;
      if (dist <= 24 || inBox) {
        draggedNodeIdxRef.current = i;
        dragOffsetRef.current = { x: x - n.x, y: y - n.y };
        drawTopology();
