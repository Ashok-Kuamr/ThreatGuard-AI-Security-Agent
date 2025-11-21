"""
Threat Detection Agent
Uses:
- FileScannerTool
- SystemAnalyzerTool
- MemoryBank
- LoggingService
"""

from tools.file_scanner import FileScannerTool
from tools.system_analyzer import SystemAnalyzerTool

class ThreatDetectionAgent:
    def __init__(self, memory_bank=None, logger=None):
        self.file_scanner = FileScannerTool()
        self.system_analyzer = SystemAnalyzerTool()
        self.memory = memory_bank
        self.logger = logger

    # -----------------------------
    # 1) Analyze a file snippet
    # -----------------------------
    def analyze_file(self, file_text: str):
        if self.logger:
            self.logger.log("Starting file analysis...")

        result = self.file_scanner.scan_text(file_text)

        if self.logger:
            self.logger.log(f"File Scan Result: {result}")

        # store findings
        if self.memory:
            self.memory.save({
                "type": "file_analysis",
                "content": result
            })

        return result

    # -----------------------------
    # 2) Analyze system configuration
    # -----------------------------
    def analyze_system(self):
        if self.logger:
            self.logger.log("Starting system configuration scan...")

        result = self.system_analyzer.scan_system()

        if self.logger:
            self.logger.log(f"System Scan Result: {result}")

        if self.memory:
            self.memory.save({
                "type": "system_analysis",
                "content": result
            })

        return result

    # -----------------------------
    # 3) Main action handler
    # -----------------------------
    def run(self, input_data: str):

        if "scan file" in input_data.lower():
            return self.analyze_file(input_data)

        elif "scan system" in input_data.lower():
            return self.analyze_system()

        else:
            unknown_msg = {"message": "Unknown request. Try 'scan file' or 'scan system'."}

            if self.logger:
                self.logger.log("Unknown command received.")

            return unknown_msg
