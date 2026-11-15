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
