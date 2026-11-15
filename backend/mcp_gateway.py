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
                "version": "1.0.0"
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

    if name == "lucen_find_tools":
        task = args.get("task", "")
        top_k = args.get("top_k", 4)
        res = engine.traverse(TraversalRequest(task=task, top_k_tools=top_k))
        
        output_payload = {
            "selected_tools": [
                {
                    "id": t.id,
                    "name": t.name,
                    "server": t.server_id,
                    "description": t.description,
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
