# system_hardener.py
"""
System Hardening Tool — applies automatic fixes based on threat findings.
This tool simulates disabling risky settings, applying patches, and enforcing security rules.
"""

import json
from typing import Dict, Any


class SystemHardener:
    def __init__(self, logger=None):
        self.logger = logger

    def run(self, threat_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulated system hardening actions based on threat information.
        """

        threat_type = threat_info.get("analysis", {}).get("severity", "low")

        actions_taken = []

        if threat_type == "high":
            actions_taken.append("Disabled risky system settings")
            actions_taken.append("Applied critical security patches")
            actions_taken.append("Locked firewall rules")
        elif threat_type == "medium":
            actions_taken.append("Enabled strict monitoring mode")
            actions_taken.append("Blocked suspicious ports")
        else:
            actions_taken.append("No major changes required")

        result = {
            "hardening_status": "completed",
            "actions": actions_taken,
        }

        if self.logger:
            self.logger.log(
                "[SystemHardener] Hardening Applied: " + json.dumps(result)
            )

        return result


# Wrapper class so ActionAgent can call easily
class HardeningExecutor:
    def __init__(self, logger=None):
        self.hardener = SystemHardener(logger)

    def apply_hardening(self, threat_info):
        return self.hardener.run(threat_info)
