# filescan.py
"""
FileScan Tool — Simulated file scanning tool for ThreatGuard.
This tool analyzes metadata, file patterns, and threat signatures.
"""

import hashlib
import json
from typing import Dict, Any


class FileScanTool:
    def __init__(self, logger=None):
        self.logger = logger

    def run(self, threat_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes incoming threat_info and produces a scan report.
        """

        metadata = threat_info.get("metadata", {})
        file_content = metadata.get("file_content", "N/A")

        # Simulated hash of the file content
        file_hash = hashlib.sha256(file_content.encode()).hexdigest()

        result = {
            "file_hash": file_hash,
            "scan_status": "clean" if "virus" not in file_content.lower() else "infected",
            "details": {
                "size": len(file_content),
                "source": threat_info.get("source"),
            }
        }

        if self.logger:
            self.logger.log("[FileScanTool] Scan Result: " + json.dumps(result))

        return result


# Helper wrapper so ActionAgent can call this tool easily
class ToolExecutor:
    def __init__(self, logger=None):
        self.file_scan_tool = FileScanTool(logger)

    def run_filescan(self, threat_info):
        return self.file_scan_tool.run(threat_info)
