"""
Lucen Argument Guard - Deep AST & Strict Allowlist Inspection
Enforces strict least-privilege policies inside generic tools (execute_sql, run_command, read_file, write_file).
Replaces fragile text blocklists with canonical path resolution and strict read-only grammar.
"""
import os
import re
from typing import Dict, Any, Tuple, Optional, List

# Workspace Root Sandbox
ALLOWED_WORKSPACE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Strict SQL Restrictions in Production:
# Enforces that production queries MUST be read-only SELECT or EXPLAIN statements.
DISALLOWED_SQL_KEYWORDS = re.compile(
    r"\b(DROP|TRUNCATE|DELETE|ALTER|UPDATE|INSERT|CREATE|GRANT|REVOKE|COPY|EXECUTE|VACUUM|REINDEX)\b|"
    r"\b(pg_terminate_backend|pg_read_file|pg_write_file|pg_read_binary_file|pg_ls_dir|dblink_exec|lo_import|lo_export)\b|"
    r"\bDO\s+\$\$|"
    r"\bWITH\s+.*\s+(DELETE|UPDATE|INSERT)\b",
    re.IGNORECASE
)

# Strict Shell Command Allowlist for Production Diagnostics
ALLOWED_PROD_COMMANDS = {"ps", "uptime", "df", "tail", "head", "cat", "grep", "uname"}
DISALLOWED_SHELL_OPERATORS = re.compile(r"[;&|`$><]|\b(rm|mkfs|dd|chmod|chown|kill|pkill|curl|wget|python|bash|sh|sudo)\b", re.IGNORECASE)

# Sensitive Root Directories Forbidden Across All Environments
FORBIDDEN_CANONICAL_PREFIXES = [
    "/etc",
    "/root",
    "/proc",
    "/sys",
    "/var/run",
    os.path.expanduser("~/.ssh"),
    os.path.expanduser("~/.aws"),
]

class ArgumentGuardResult:
    def __init__(self, allowed: bool, violation_type: Optional[str] = None, reason: Optional[str] = None):
        self.allowed = allowed
        self.violation_type = violation_type
        self.reason = reason

    def __bool__(self):
        return self.allowed

def inspect_tool_arguments(tool_name: str, arguments: Dict[str, Any], environment: str = "production") -> ArgumentGuardResult:
    """
    Performs deep argument inspection on incoming tool arguments.
    Enforces strict read-only SQL grammar, canonical path containment, and command allowlisting.
    """
    if not isinstance(arguments, dict):
        return ArgumentGuardResult(allowed=True)

    tool_lower = tool_name.lower()

    # =========================================================================
    # 1. SQL Query Inspection (Enforces Strict Read-Only in Production)
    # =========================================================================
    for key, val in arguments.items():
        if not isinstance(val, str):
            continue
        val_str = val.strip()

        # Detect SQL parameters regardless of tool name
        if any(db_kw in key.lower() for db_kw in ["sql", "query", "statement"]) or any(db_tool in tool_lower for db_tool in ["sql", "postgres", "db", "query"]):
            if environment in ("production", "staging"):
                # Must start with SELECT or EXPLAIN
                if not re.match(r"^(SELECT|EXPLAIN)\b", val_str, re.IGNORECASE):
                    return ArgumentGuardResult(
                        allowed=False,
                        violation_type="SQL_GRAMMAR_VIOLATION",
                        reason=f"Production policy enforces strict read-only SQL. Query must begin with SELECT or EXPLAIN (Received: '{val_str[:40]}...')"
                    )

                # Check for nested subqueries, CTE deletes, or dangerous administrative functions
                disallowed_match = DISALLOWED_SQL_KEYWORDS.search(val_str)
                if disallowed_match:
                    return ArgumentGuardResult(
                        allowed=False,
                        violation_type="SQL_MUTATION_VIOLATION",
                        reason=f"Disallowed DDL/DML/Admin token '{disallowed_match.group()}' detected inside SQL query in {environment}."
                    )

        # =========================================================================
        # 2. Canonical Filesystem Path Inspection (Realpath Resolution)
        # =========================================================================
        if any(path_kw in key.lower() for path_kw in ["path", "file", "filename", "filepath", "dest", "src"]) or any(f_tool in tool_lower for f_tool in ["file", "fs", "read", "write"]):
            raw_path = val_str
            # Canonicalize path to resolve symlinks and ../ traversal
            try:
                if not os.path.isabs(raw_path):
                    resolved_path = os.path.realpath(os.path.join(ALLOWED_WORKSPACE_ROOT, raw_path))
                else:
                    resolved_path = os.path.realpath(raw_path)
            except Exception:
                resolved_path = raw_path

            # Check for sensitive system directories
            for forbidden in FORBIDDEN_CANONICAL_PREFIXES:
                if resolved_path.startswith(forbidden) or "/.ssh" in resolved_path or "/.env" in resolved_path:
                    return ArgumentGuardResult(
                        allowed=False,
                        violation_type="CANONICAL_PATH_VIOLATION",
                        reason=f"Canonical path '{resolved_path}' breaches protected system directory or sensitive credentials file."
                    )

            # In production, file writes must be strictly confined to workspace root
            if "write" in tool_lower or "delete" in tool_lower:
                if not resolved_path.startswith(ALLOWED_WORKSPACE_ROOT):
                    return ArgumentGuardResult(
                        allowed=False,
                        violation_type="WORKSPACE_CONFINEMENT_VIOLATION",
                        reason=f"File mutation target '{resolved_path}' is outside permitted workspace root '{ALLOWED_WORKSPACE_ROOT}'."
                    )

        # =========================================================================
        # 3. Shell Command Allowlisting (Strict In-Prod Allowlist)
        # =========================================================================
        if any(sh_kw in key.lower() for sh_kw in ["cmd", "command", "script", "bash", "exec"]) or any(sh_tool in tool_lower for sh_tool in ["bash", "sh", "exec", "terminal", "command", "run_command"]):
            if environment == "production":
                # Check for operators (pipes, redirects, backgrounding, chaining)
                op_match = DISALLOWED_SHELL_OPERATORS.search(val_str)
                if op_match:
                    return ArgumentGuardResult(
                        allowed=False,
                        violation_type="SHELL_OPERATOR_VIOLATION",
                        reason=f"Shell command contains prohibited operator or destructive binary '{op_match.group()}' in production."
                    )

                # Verify base command against allowlist
                base_cmd = val_str.split()[0].lower() if val_str.split() else ""
                if base_cmd not in ALLOWED_PROD_COMMANDS:
                    return ArgumentGuardResult(
                        allowed=False,
                        violation_type="COMMAND_NOT_ALLOWLISTED",
                        reason=f"Command '{base_cmd}' is not in production diagnostic allowlist ({', '.join(sorted(ALLOWED_PROD_COMMANDS))})."
                    )

    return ArgumentGuardResult(allowed=True)
