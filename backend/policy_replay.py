"""
Lucen Policy Replay - Pre-Deployment Impact Simulation
------------------------------------------------------
Replays historical audit logs against candidate policy files (lucen.policy.yaml)
to simulate production impact, measure rule precision, and quantify false-positive rates
before enforcing new governance boundaries.
"""

import os
import json
import yaml
from typing import Dict, Any, List, Tuple, Optional

AUDIT_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lucen_audit.jsonl")
DEFAULT_POLICY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lucen.policy.yaml")

def run_policy_replay(policy_path: Optional[str] = None, log_path: Optional[str] = None) -> Dict[str, Any]:
    policy_file = policy_path or DEFAULT_POLICY_FILE
    audit_file = log_path or AUDIT_LOG_FILE

    if not os.path.exists(policy_file):
        return {"error": f"Policy file not found: {policy_file}"}
    if not os.path.exists(audit_file):
        return {"error": f"Audit log not found: {audit_file}"}

    with open(policy_file, "r", encoding="utf-8") as f:
        policy = yaml.safe_load(f) or {}

    prod_deny_tools = policy.get("environments", {}).get("production", {}).get("deny_tools", [])
    prod_approval_tools = policy.get("environments", {}).get("production", {}).get("require_human_approval", [])

    total_evaluated = 0
    originally_allowed = 0
    originally_blocked = 0
    replay_would_block = 0
    replay_would_approve = 0
    replay_would_allow = 0

    blocked_breakdown: Dict[str, int] = {}

    with open(audit_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue

            total_evaluated += 1
            tool = entry.get("tool_called", "")
            orig_verdict = entry.get("verdict", "ALLOWED")
            env = entry.get("environment", "production")

            if orig_verdict == "ALLOWED":
                originally_allowed += 1
            else:
                originally_blocked += 1

            # Simulate evaluation in production
            is_denied = False
            is_approval = False

            if env == "production":
                for dt in prod_deny_tools:
                    pattern = dt.replace("*", "")
                    if pattern in tool:
                        is_denied = True
                        blocked_breakdown[dt] = blocked_breakdown.get(dt, 0) + 1
                        break

                if not is_denied:
                    for at in prod_approval_tools:
                        pattern = at.replace("*", "")
                        if pattern in tool:
                            is_approval = True
                            break

            if is_denied:
                replay_would_block += 1
            elif is_approval:
                replay_would_approve += 1
            else:
                replay_would_allow += 1

    false_positive_pct = round((replay_would_block / max(1, originally_allowed)) * 100, 2)

    return {
        "status": "success",
        "policy_evaluated": os.path.basename(policy_file),
        "total_historical_events": total_evaluated,
        "originally_allowed": originally_allowed,
        "originally_blocked": originally_blocked,
        "simulated_allowed": replay_would_allow,
        "simulated_paused_for_approval": replay_would_approve,
        "simulated_blocked": replay_would_block,
        "false_positive_rate_pct": false_positive_pct,
        "rule_breakdown": blocked_breakdown
    }
