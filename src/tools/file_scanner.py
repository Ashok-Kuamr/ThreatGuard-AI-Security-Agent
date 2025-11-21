# file_scanner.py
"""
Simulated File Scanner Tool for ThreatGuard.
Reads text, detects suspicious patterns, and returns structured results.
"""

import re
from typing import Dict, Any


class FileScannerTool:
    def __init__(self):
        pass

    def scan_text(self, text: str) -> Dict[str, Any]:
        findings = []

        suspicious_patterns = {
            "SQL Injection": r"(DROP TABLE|UNION SELECT|--|;--)",
            "XSS": r"(<script>|javascript:)",
            "Hardcoded Password": r"(password\s*=|pwd\s*=|\"password\")",
            "Dangerous API": r"(eval\(|exec\()",
        }

        for threat_name, pattern in suspicious_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                findings.append(threat_name)

        return {
            "raw_text_length": len(text),
            "detected_issues": findings,
            "severity": "HIGH" if findings else "LOW"
        }
