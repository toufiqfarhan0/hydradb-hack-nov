"""
Lucen Ephemeral Database Roles - Engine-Level Defense-in-Depth for PostgreSQL
Creates short-lived, least-privilege PostgreSQL roles per task session.
Enforces that even if application-level SQL parsing is bypassed, the PostgreSQL storage engine
itself rejects DROP, DELETE, TRUNCATE, and ALTER at the database permission level.
"""

import time
import secrets
from typing import Dict, Any, Optional

class EphemeralRoleManager:
    def __init__(self):
        self.active_roles: Dict[str, Dict[str, Any]] = {}

    def generate_task_role(
        self,
        task_id: str,
        database: str = "hydra_analytics",
        ttl_seconds: int = 300,
        read_only: bool = True
    ) -> Dict[str, Any]:
        """
        Generates an ephemeral, single-task database role with strict validity window and read-only grant.
        """
        token = secrets.token_hex(6)
        role_name = f"lucen_agent_{token}"
        password = secrets.token_urlsafe(24)
        expires_at = time.time() + ttl_seconds
        valid_until_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(expires_at))

        # Strict least-privilege PostgreSQL grant specification
        if read_only:
            ddl_statements = [
                f"CREATE ROLE {role_name} WITH LOGIN PASSWORD '{password}' VALID UNTIL '{valid_until_str}';",
                f"GRANT CONNECT ON DATABASE {database} TO {role_name};",
                f"GRANT USAGE ON SCHEMA public TO {role_name};",
                f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {role_name};",
                f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {role_name};",
                f"REVOKE ALL ON SCHEMA information_schema FROM {role_name};"
            ]
            privilege_tier = "SELECT_ONLY_DIAGNOSTIC"
        else:
            ddl_statements = [
                f"CREATE ROLE {role_name} WITH LOGIN PASSWORD '{password}' VALID UNTIL '{valid_until_str}';",
                f"GRANT CONNECT ON DATABASE {database} TO {role_name};",
                f"GRANT USAGE ON SCHEMA public TO {role_name};",
                f"GRANT SELECT, UPDATE, INSERT ON ALL TABLES IN SCHEMA public TO {role_name};"
            ]
            privilege_tier = "MUTATING_OPERATOR_RESTRICTED"

        role_record = {
            "role_name": role_name,
            "username": role_name,
            "password": password,
            "database": database,
            "privilege_tier": privilege_tier,
            "created_at": time.time(),
            "expires_at": expires_at,
            "valid_until": valid_until_str,
            "ddl_statements": ddl_statements,
            "status": "ACTIVE_EPHEMERAL"
        }

        self.active_roles[role_name] = role_record
        return role_record

    def verify_role_validity(self, role_name: str) -> bool:
        """Verify role has not expired past its TTL."""
        role = self.active_roles.get(role_name)
        if not role:
            return False
        return time.time() <= role["expires_at"]

# Global Singleton Manager
ephemeral_role_manager = EphemeralRoleManager()
