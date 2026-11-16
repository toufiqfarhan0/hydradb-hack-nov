"""
Lucen MCP Gateway — Model Context Protocol Stdio Server
Acts as an intelligent context proxy and tool router for autonomous agents.
Compatible with Claude Desktop, Cursor, Continue, and standard MCP clients.

Configuration in claude_desktop_config.json:
{
  "mcpServers": {
    "lucen": {
      "command": "python",
      "args": ["-m", "backend.mcp_gateway"]
    }
  }
}
"""
import sys
import os
import json
from typing import Dict, Any, Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.hydradb_engine import HydraDBContextEngine
from backend.models import TraversalRequest, FeedbackRequest

def write_jsonrpc_response(res: Dict[str, Any]):
    """Write standard JSON-RPC line to stdout."""
    line = json.dumps(res) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()

def handle_initialize(msg_id: Any) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "lucen-hydradb-gateway",
                "version": "1.2.0"
            }
        }
    }

def handle_tools_list(msg_id: Any) -> Dict[str, Any]:
    tools = [
        {
            "name": "lucen_find_tools",
            "description": (
                "Traverse the HydraDB property graph to isolate the exact tools and pre-bound "
                "runtime credentials required for an agent task. Prunes 99.6% of prompt context "
                "tokens and prevents LLM parameter hallucination."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Natural language operational task (e.g. 'Postgres connection pool leak in prod')"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of tools to isolate (default: 4)",
                        "default": 4
                    }
                },
                "required": ["task"]
            }
        },
        {
            "name": "lucen_record_feedback",
            "description": (
                "Record execution feedback in HydraDB continual learning memory. Dynamically "
                "increments PREFERS edge weights via atomic OpenCypher SET commands for successful calls."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "tool_id": {
                        "type": "string",
                        "description": "ID of the tool invoked (e.g. 'tool_pg_check_connection_pool')"
                    },
                    "success": {
                        "type": "boolean",
                        "description": "True if tool invocation succeeded, False if failed"
                    },
                    "task": {
                        "type": "string",
                        "description": "The task query associated with the invocation"
                    }
                },
                "required": ["tool_id", "success", "task"]
            }
        },
        {
            "name": "lucen_expand",
            "description": (
                "Escape hatch: If candidate tools appear insufficient, widens context to 1-hop "
                "and 2-hop adjacent tools via [:CHAINED_TO] workflows and shared capabilities."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "tools": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of current tool IDs to expand from"
                    },
                    "task": {
                        "type": "string",
                        "description": "Optional task context for relevance scoring"
                    }
                },
                "required": ["tools"]
            }
        },
        {
            "name": "lucen_blast_radius",
            "description": (
                "Compute operational dependency impact and blast radius before executing a tool."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "tool": {
                        "type": "string",
                        "description": "Tool name or ID to analyze"
                    }
                },
                "required": ["tool"]
            }
        },
        {
            "name": "pg_check_connection_pool",
            "description": (
                "Inspect PostgreSQL database connection pool utilization, idle timeouts, and waiting clients. "
                "Requires host parameter pre-bound by Lucen."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string",
                        "description": "PostgreSQL cluster host endpoint (e.g. 'pg-cluster-prod.internal:5432')"
                    },
                    "database": {
                        "type": "string",
                        "description": "Target database name (default: 'hydra_analytics')",
                        "default": "hydra_analytics"
                    }
                },
                "required": ["host"]
            }
        },
        {
            "name": "slack_post_incident_bulletin",
            "description": (
                "Broadcast a structured incident bulletin to a target war-room Slack channel with live thread status."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "channel_id": {
                        "type": "string",
                        "description": "Pre-bound Slack channel ID (e.g. 'C08A91KL2')"
                    },
                    "title": {
                        "type": "string",
                        "description": "Incident bulletin title"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["P0", "P1", "P2", "INFO"],
                        "default": "P0"
                    },
                    "message": {
                        "type": "string",
                        "description": "Markdown formatted incident report and mitigation steps"
                    }
                },
                "required": ["channel_id", "title", "message"]
            }
        },
        {
            "name": "sqlite_query",
            "description": "Execute a read-only SQL query against local SQLite diagnostics store.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Read-only SQL query string (SELECT only)"
                    }
                },
                "required": ["query"]
            }
        }
    ]
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {
            "tools": tools
        }
    }

def handle_tools_call(msg_id: Any, params: Dict[str, Any], engine: HydraDBContextEngine) -> Dict[str, Any]:
    name = params.get("name")
    args = params.get("arguments", {})
    engine_served_by = "hydradb_cluster" if engine.connected_live else "local_csr"
    active_env = os.environ.get("LUCEN_ENVIRONMENT", "production")
    mode = os.environ.get("LUCEN_MODE", "enforce")  # 'enforce' or 'shadow'

    # 1. Call-Time Zero-Trust Enforcement: Deny destructive/blocked tools even if directly invoked
    if name not in ("lucen_find_tools", "lucen_record_feedback", "lucen_expand", "lucen_blast_radius"):
        tool_node = engine.tools.get(f"tool_{name}") or next((t for t in engine.tools.values() if t.name == name), None)
        if tool_node:
            if active_env not in tool_node.allowed_environments or (tool_node.destructive and active_env == "production"):
                from backend.audit_trail import append_audit_entry
                append_audit_entry(
                    task=f"Direct Execution Attempt: {name}",
                    tool_called=name,
                    environment=active_env,
                    verdict="SHADOW_ALERT" if mode == "shadow" else "BLOCKED",
                    details={"reason": f"Tool '{name}' is blocked by Lucen Zero-Trust policy in environment '{active_env}'"}
                )
                if mode != "shadow":
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {
                            "code": -32001,
                            "message": f"PERMISSION_DENIED: Tool '{name}' is blocked by Lucen Zero-Trust policy in environment '{active_env}'. Execution halted."
                        }
                    }

        # 2. Deep Argument-Level Inspection (AST & Pattern Checking for SQL, Paths, Shell)
        from backend.argument_guard import inspect_tool_arguments
        arg_check = inspect_tool_arguments(name, args, active_env)
        if not arg_check.allowed:
            from backend.audit_trail import append_audit_entry
            append_audit_entry(
                task=f"Argument Attack Attempt: {name}",
                tool_called=name,
                environment=active_env,
                verdict="SHADOW_ALERT" if mode == "shadow" else "BLOCKED",
                details={"violation": arg_check.violation_type, "reason": arg_check.reason}
            )
            if mode != "shadow":
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32002,
                        "message": f"PERMISSION_DENIED: {arg_check.reason}"
                    }
                }

        # 3. Session Taint Tracking & Exfiltration Protection
        session_id = os.environ.get("LUCEN_SESSION_ID", "default_agent_session")
        if tool_node:
            session = engine.session_taints[session_id]
            # Only confidential customer data taints the session (operational telemetry does not)
            if tool_node.reads_private_data:
                session["is_tainted"] = True
                session["taint_type"] = "CONFIDENTIAL_CUSTOMER_DATA"
                session["sources"].append(tool_node.name)

            # Destination Whitelisting: Approved internal war rooms vs untrusted public sinks
            target_dest = str(args.get("channel_id", "") or args.get("channel", "") or args.get("url", "")).lower()
            is_approved_internal_sink = any(app_sink in target_dest for app_sink in ["incident", "war-room", "c08a91kl2", "internal", "ops"])

            if tool_node.external_facing and session["is_tainted"]:
                # If target is an approved internal war-room channel and action is operational bulletin, allow it
                if is_approved_internal_sink and "bulletin" in tool_node.name:
                    pass
                else:
                    allow_exfil = os.environ.get("LUCEN_ALLOW_EXFILTRATION", "false").lower() == "true"
                    if not allow_exfil:
                        from backend.audit_trail import append_audit_entry
                        reason = (
                            f"Data exfiltration blocked: Session tainted by [{', '.join(session['sources'][:2])}] "
                            f"attempted to transmit data to unapproved sink '{target_dest or name}' without human approval"
                        )
                        append_audit_entry(
                            task=f"Exfiltration Attempt: {name}",
                            tool_called=name,
                            environment=active_env,
                            verdict="SHADOW_ALERT" if mode == "shadow" else "BLOCKED",
                            details={"violation": "DATA_FLOW_EXFILTRATION", "reason": reason}
                        )
                        if mode != "shadow":
                            return {
                                "jsonrpc": "2.0",
                                "id": msg_id,
                                "error": {
                                    "code": -32003,
                                    "message": f"PERMISSION_DENIED: {reason}"
                                }
                            }


    if name == "lucen_find_tools":
        task = args.get("task", "")
        top_k = args.get("top_k", 4)
        env = args.get("environment", "production")
        allow_destructive = args.get("allow_destructive", False)
        res = engine.traverse(TraversalRequest(task=task, top_k_tools=top_k, environment=env, allow_destructive=allow_destructive))
        
        output_payload = {
            "engine_served_by": engine_served_by,
            "environment": env,
            "security_perimeter_active": True,
            "pruned_for_security": res.pruned_for_security,
            "selected_tools": [
                {
                    "id": t.id,
                    "name": t.name,
                    "server": t.server_id,
                    "description": t.description,
                    "mutating": t.mutating,
                    "destructive": t.destructive,
                    "schema_hash": t.schema_hash,
                    "secret_handles": t.secret_handles,
                    "estimated_tokens": t.estimated_token_cost
                }
                for t in res.selected_tools
            ],
            "pre_bound_entities": [
                {
                    "id": e.id,
                    "name": e.name,
                    "type": e.entity_type,
                    "properties": e.properties
                }
                for e in res.resolved_entities
            ],
            "token_reduction_pct": res.token_reduction_pct,
            "traversal_latency_ms": res.traversal_latency_ms,
            "opencypher_query": res.opencypher_query
        }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(output_payload, indent=2)
                    }
                ]
            }
        }

    elif name == "lucen_record_feedback":
        tool_id = args.get("tool_id", "")
        success = args.get("success", True)
        task = args.get("task", "agent invocation")
        fb = engine.record_feedback(FeedbackRequest(tool_id=tool_id, success=success, task=task))
        fb["engine_served_by"] = engine_served_by
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(fb, indent=2)
                    }
                ]
            }
        }

    elif name == "lucen_expand":
        from backend.models import ExpandRequest
        seed_tools = args.get("tools", [])
        task = args.get("task", "")
        exp_res = engine.expand_tools(ExpandRequest(current_tools=seed_tools, task_context=task))
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "original_tools": exp_res.original_tools,
                            "expanded_tools": [
                                {
                                    "id": t.id,
                                    "name": t.name,
                                    "server": t.server_id,
                                    "description": t.description
                                }
                                for t in exp_res.expanded_tools
                            ],
                            "rationale": exp_res.expansion_rationale,
                            "expansion_latency_ms": exp_res.expansion_latency_ms
                        }, indent=2)
                    }
                ]
            }
        }

    elif name == "lucen_blast_radius":
        tool_target = args.get("tool", "")
        blast = engine.get_blast_radius(tool_target)
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "tool_id": blast.tool_id,
                            "tool_name": blast.tool_name,
                            "action_type": blast.action_type,
                            "risk_level": blast.risk_level,
                            "requires_human_approval": blast.requires_human_approval,
                            "impacted_services": blast.impacted_services,
                            "data_assets_at_risk": blast.data_assets_at_risk,
                            "dependent_tools_count": len(blast.dependent_tools_affected),
                            "blast_summary": blast.blast_summary
                        }, indent=2)
                    }
                ]
            }
        }


    elif name == "pg_check_connection_pool":
        host = args.get("host", "pg-cluster-prod.internal:5432")
        db = args.get("database", "hydra_analytics")
        
        result_data = {
            "status": "warning",
            "simulated": True,
            "transport": "mock_upstream",
            "host": host,
            "database": db,
            "max_connections": 400,
            "active_connections": 387,
            "idle_connections": 13,
            "waiting_clients": 42,
            "pool_utilization_pct": 96.75,
            "recommendation": "Active connection pool near exhaustion. Execute idle connection purge or scale read replicas.",
            "engine_served_by": engine_served_by
        }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result_data, indent=2)
                    }
                ]
            }
        }

    elif name == "slack_post_incident_bulletin":
        channel_id = args.get("channel_id", "C08A91KL2")
        title = args.get("title", "P0 Incident Bulletin")
        severity = args.get("severity", "P0")
        message = args.get("message", "")

        result_data = {
            "status": "delivered",
            "simulated": True,
            "transport": "mock_upstream",
            "channel_id": channel_id,
            "severity": severity,
            "timestamp": "1731638400.019200",
            "bulletin_title": title,
            "engine_served_by": engine_served_by
        }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result_data, indent=2)
                    }
                ]
            }
        }

    elif name == "sqlite_query":
        query = args.get("query", "SELECT * FROM services;")
        import sqlite3
        try:
            conn = sqlite3.connect(":memory:")
            c = conn.cursor()
            c.execute("CREATE TABLE services (id INT, service TEXT, status TEXT, latency_p99_ms REAL);")
            c.execute("INSERT INTO services VALUES (1, 'hydra-router', 'healthy', 0.72), (2, 'hydra-worker', 'degraded', 14.8), (3, 'pgbouncer-pool', 'exhausted', 184.2);")
            if query.strip().upper().startswith("SELECT"):
                cur = c.execute(query)
                cols = [desc[0] for desc in cur.description]
                rows = [dict(zip(cols, row)) for row in cur.fetchall()]
            else:
                rows = []
            conn.close()
            status = "success"
        except Exception as e:
            rows = []
            status = f"error: {str(e)}"

        result_data = {
            "status": status,
            "simulated": False,
            "transport": "local_sqlite_engine",
            "query": query,
            "rows": rows,
            "row_count": len(rows),
            "engine_served_by": engine_served_by
        }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result_data, indent=2)
                    }
                ]
            }
        }

    else:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Method {name} not found"
            }
        }

def run_mcp_gateway():
    """Main stdio loop for Model Context Protocol JSON-RPC."""
    engine = HydraDBContextEngine()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        msg_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            write_jsonrpc_response(handle_initialize(msg_id))
        elif method == "notifications/initialized":
            pass # Notification, no response required
        elif method == "tools/list":
            write_jsonrpc_response(handle_tools_list(msg_id))
        elif method == "tools/call":
            write_jsonrpc_response(handle_tools_call(msg_id, params, engine))
        elif method == "ping":
            write_jsonrpc_response({"jsonrpc": "2.0", "id": msg_id, "result": {}})
        else:
            if msg_id is not None:
                write_jsonrpc_response({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method {method} not supported"
                    }
                })

if __name__ == "__main__":
    run_mcp_gateway()
