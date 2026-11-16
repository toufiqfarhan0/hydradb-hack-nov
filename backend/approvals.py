"""
Lucen Human-in-the-Loop Approval Workflow
-------------------------------------------------------------
Manages authorization gates for high-blast-radius or mutating production actions.
Every approval verdict is cryptographically signed and chained into the audit ledger.
"""

import os
import json
import time
import secrets
from typing import Dict, Any, List, Optional

APPROVALS_STORE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".lucen_approvals.json")

class ApprovalManager:
    def __init__(self):
        self._load()

    def _load(self):
        if os.path.exists(APPROVALS_STORE):
            try:
                with open(APPROVALS_STORE, "r", encoding="utf-8") as f:
                    self.approvals = json.load(f)
            except Exception:
                self.approvals = {}
        else:
            self.approvals = {}

    def _save(self):
        with open(APPROVALS_STORE, "w", encoding="utf-8") as f:
            json.dump(self.approvals, f, indent=2)

    def create_request(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        environment: str = "production",
        blast_summary: str = "",
        impacted_services: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        req_id = f"REQ-{secrets.token_hex(4).upper()}"
        now_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        record = {
            "request_id": req_id,
            "tool_name": tool_name,
            "arguments": arguments,
            "environment": environment,
            "blast_summary": blast_summary,
            "impacted_services": impacted_services or [],
            "status": "PENDING_APPROVAL",
            "created_at": now_str,
            "resolved_at": None,
            "approver": None,
            "audit_hash": None
        }

        self.approvals[req_id] = record
        self._save()

        # Log pending gate in audit ledger
        from backend.audit_trail import append_audit_entry
        entry = append_audit_entry(
            task=f"Human Gate Paused: {tool_name}",
            tool_called=tool_name,
            environment=environment,
            verdict="GATE_PAUSED",
            details={"request_id": req_id, "blast_summary": blast_summary}
        )
        record["audit_hash"] = entry.get("entry_hash")
        self._save()

        return record

    def approve_request(self, request_id: str, approver: str = "ops_admin") -> Dict[str, Any]:
        self._load()
        req = self.approvals.get(request_id)
        if not req:
            return {"error": f"Request {request_id} not found"}

        now_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        req["status"] = "APPROVED"
        req["approver"] = approver
        req["resolved_at"] = now_str

        from backend.audit_trail import append_audit_entry
        entry = append_audit_entry(
            task=f"Human Gate Approved: {req['tool_name']} by {approver}",
            tool_called=req["tool_name"],
            environment=req["environment"],
            verdict="HUMAN_APPROVED",
            details={"request_id": request_id, "approved_by": approver}
        )
        req["audit_hash"] = entry.get("entry_hash")
        self._save()
        return req

    def reject_request(self, request_id: str, approver: str = "ops_admin", reason: str = "") -> Dict[str, Any]:
        self._load()
        req = self.approvals.get(request_id)
        if not req:
            return {"error": f"Request {request_id} not found"}

        now_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        req["status"] = "REJECTED"
        req["approver"] = approver
        req["resolved_at"] = now_str
        req["rejection_reason"] = reason

        from backend.audit_trail import append_audit_entry
        entry = append_audit_entry(
            task=f"Human Gate Rejected: {req['tool_name']} by {approver}",
            tool_called=req["tool_name"],
            environment=req["environment"],
            verdict="HUMAN_REJECTED",
            details={"request_id": request_id, "rejected_by": approver, "reason": reason}
        )
        req["audit_hash"] = entry.get("entry_hash")
        self._save()
        return req

    def list_requests(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        self._load()
        items = list(self.approvals.values())
        if status:
            items = [i for i in items if i.get("status") == status]
        return items

# Global Singleton Manager
approval_manager = ApprovalManager()
