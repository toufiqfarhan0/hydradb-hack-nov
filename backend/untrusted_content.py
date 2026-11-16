"""
Lucen Untrusted Content Shield - Defense Against the "Lethal Trifecta"
---------------------------------------------------------------------
The "Lethal Trifecta" in Autonomous Agents occurs when three conditions align:
  1. Access to Private Internal Data (PostgreSQL, production logs, AWS secrets)
  2. Ingestion of Untrusted External Content (GitHub issues, emails, web pages, ticket text)
  3. Access to an Outbound Transmission Sink (Slack, Webhook, GitHub PR, Email)

When untrusted external input enters an agent session, this module tags the session
context as EXPOSED_TO_UNTRUSTED_INPUT. Any attempt to pipe data to an outbound sink
triggers mandatory human approval and pauses execution.
"""

import re
from typing import Dict, Any, List, Optional, Tuple

# Patterns identifying external/untrusted content vectors
UNTRUSTED_SOURCE_MARKERS = [
    re.compile(r"\b(github_issue|sentry_ticket|jira_issue|user_email|web_page|scraped_content|customer_ticket)\b", re.IGNORECASE),
    re.compile(r"\b(ticket\s+description|issue\s+body|webhook\s+payload|external\s+comment)\b", re.IGNORECASE)
]

# Canary phrases indicating adversarial prompt injection inside untrusted content
INJECTION_CANARY_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
    re.compile(r"system\s+(override|prompt|directive)", re.IGNORECASE),
    re.compile(r"exfiltrate\s+to", re.IGNORECASE),
    re.compile(r"send\s+.*(password|secret|key|vault|credential)\s+to", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+in\s+developer\s+mode", re.IGNORECASE)
]

class UntrustedContentShield:
    def __init__(self):
        # session_id -> {"has_untrusted_input": bool, "source_desc": str, "canary_tripped": bool}
        self.session_states: Dict[str, Dict[str, Any]] = {}

    def scan_and_tag_input(self, session_id: str, input_text: str, source_label: Optional[str] = None) -> Dict[str, Any]:
        """
        Scans an incoming input payload for untrusted content markers and prompt injection canaries.
        Tags the session if untrusted content is detected.
        """
        is_untrusted = False
        canary_tripped = False
        matched_canary = None

        # Check explicit source label
        if source_label and any(src in source_label.lower() for src in ["ticket", "issue", "email", "web", "untrusted", "sentry"]):
            is_untrusted = True

        # Check for untrusted content markers in text
        for marker in UNTRUSTED_SOURCE_MARKERS:
            if marker.search(input_text):
                is_untrusted = True
                break

        # Scan for injection canaries
        for canary in INJECTION_CANARY_PATTERNS:
            match = canary.search(input_text)
            if match:
                canary_tripped = True
                is_untrusted = True
                matched_canary = match.group()
                break

        state = {
            "session_id": session_id,
            "has_untrusted_input": is_untrusted,
            "canary_tripped": canary_tripped,
            "matched_canary": matched_canary,
            "source_label": source_label or ("untrusted_external" if is_untrusted else "trusted_operator")
        }
        self.session_states[session_id] = state
        return state

    def check_lethal_trifecta(
        self,
        session_id: str,
        session_has_private_data: bool,
        target_tool_is_external_sink: bool
    ) -> Tuple[bool, Optional[str]]:
        """
        Evaluates the Lethal Trifecta condition:
        (Private Data Present) + (Untrusted Input Ingested) + (Outbound Sink Target)
        Returns (is_trifecta_triggered, halt_reason)
        """
        session_state = self.session_states.get(session_id, {"has_untrusted_input": False, "canary_tripped": False})
        has_untrusted = session_state.get("has_untrusted_input", False)

        if session_has_private_data and has_untrusted and target_tool_is_external_sink:
            canary_note = f" (Injection signature: '{session_state.get('matched_canary')}')" if session_state.get('canary_tripped') else ""
            reason = (
                f"LETHAL TRIFECTA BLOCKED: Session holds private internal data and has ingested untrusted "
                f"external content{canary_note}. Dispatch to outbound sink is halted pending human authorization."
            )
            return True, reason

        return False, None

# Global Singleton Shield
untrusted_content_shield = UntrustedContentShield()
