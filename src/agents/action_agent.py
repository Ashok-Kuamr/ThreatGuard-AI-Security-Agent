# action_agent.py
"""
ActionAgent for executing automated responses
based on the threat category identified by ThreatClassifierAgent.
"""

import json
from typing import Dict, Any


class ActionAgent:
    def __init__(self, tool_executor=None, memory_agent=None, logger=None):
        """
        tool_executor: object that exposes functions to run tools (filescan, code-exec, etc.)
        memory_agent: object for saving threat history/logs
        logger: logging utility
        """
        self.tool_executor = tool_executor
        self.memory = memory_agent
        self.logger = logger

    def execute_action(self, threat_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute action based on classified threat.
        
        threat_info example:
        {
            "threat_type": "malware",
            "severity": "high",
            "source": "file_upload",
            "metadata": {...}
        }
        """
        threat_type = threat_info.get("threat_type")
        severity = threat_info.get("severity")
        source = threat_info.get("source")

        # Logging the decision
        if self.logger:
            self.logger.log(f"[ActionAgent] Received threat: {json.dumps(threat_info)}")

        result = {"action_taken": None, "details": {}}

        # -------------------------
        # ACTION 1 — FILE SCAN
        # -------------------------
        if threat_type in ["malware", "suspicious_file"]:
            if self.tool_executor:
                scan_result = self.tool_executor.run_filescan(threat_info)
                result["action_taken"] = "filescan"
                result["details"] = scan_result

        # -------------------------
        # ACTION 2 — BLOCK
        # -------------------------
        if severity == "high":
            result["action_taken"] = "blocked"
            result["details"] = {"reason": "High severity threat blocked."}

        # -------------------------
        # ACTION 3 — SAVE MEMORY
        # -------------------------
        if self.memory:
            self.memory.store(threat_info)

        # -------------------------
        # ACTION 4 — ALERT
        # -------------------------
        if self.logger:
            self.logger.log(f"[ActionAgent] Action taken: {result}")

        return result
