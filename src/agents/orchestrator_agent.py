"""
OrchestratorAgent
Wires together:
 - ThreatDetectionAgent
 - ActionAgent
 - MemoryBank
 - Tools (FileScan Tool / System Hardener)
 - Logger
Provides a single `run()` that demonstrates an example pipeline.
"""

# Use imports that match the repository layout (src is the package root when run correctly).
from agents.gemini_agent import GeminiAnalysisAgent
from agents.threat_detection_agent import ThreatDetectionAgent
from agents.action_agent import ActionAgent
from memory.memory_bank import MemoryBank
from utils.logger import ThreatLogger

# Tools
from tools.filescan import ToolExecutor as FileToolExecutor
from tools.system_hardener import HardeningExecutor

class OrchestratorAgent:
    def __init__(self):
        # Core infra
        self.logger = ThreatLogger(store_in_memory=True)
        self.memory = MemoryBank()

        # Tools
        self.file_tool = FileToolExecutor(logger=self.logger)    # filescan.ToolExecutor
        self.hardener = HardeningExecutor(logger=self.logger)    # system_hardener.HardeningExecutor

        # Agents
        self.threat_agent = ThreatDetectionAgent(memory_bank=self.memory, logger=self.logger)
        self.action_agent = ActionAgent(tool_executor=self.file_tool, memory_agent=self.memory, logger=self.logger)

                # Gemini agent (LLM) - optional, safe fallback if no key
        self.gemini_agent = GeminiAnalysisAgent(logger=self.logger)


        self.logger.log("🧠 Orchestrator initialized with agents & tools.")

    def run_demo_pipeline(self):
        """
        Run a short demo pipeline illustrating:
         1) file analysis
         2) threat classification result
         3) action execution
         4) memory & logs
        """

        self.logger.log("🔄 Starting demo pipeline...")

        # Example 1: File scan flow
        example_file_text = (
            "User uploaded file with suspicious content: eval(console.log('hacked')); "
            "Potential hardcoded password: password = '1234';"
        )
        self.logger.log("📁 Demo: Running file analysis on example payload.")
        file_result = self.threat_agent.analyze_file(example_file_text)

     
        # Normalize threat_info for action agent
        threat_info = {
            "threat_type": "suspicious_file" if file_result.get("detected_issues") else "benign",
            "severity": "high" if file_result.get("detected_issues") else "low",
            "source": "demo_file_upload",
            "metadata": {
                "file_content": example_file_text,
                "file_scan": file_result
            }
        }

        # --- Optional: Gemini-powered extra analysis for file ---
        self.logger.log("🧠 Running Gemini analysis for file content (if enabled).")
        gemini_file_analysis = self.gemini_agent.analyze_file_with_gemini(example_file_text)
        self.logger.log(f"[GeminiAgent] File analysis summary: {gemini_file_analysis.get('summary') if isinstance(gemini_file_analysis, dict) else gemini_file_analysis}")
        # Attach to threat_info metadata
        threat_info["metadata"]["gemini"] = gemini_file_analysis

     
     
        # Action execution based on threat_info
        self.logger.log("🛠️ Passing classification to ActionAgent for remediation.")
        action_result = self.action_agent.execute_action(threat_info)

        # Save to memory bank (also used by ThreatDetectionAgent)
        self.memory.save_threat({
            "file_result": file_result,
            "threat_info": threat_info,
            "action_result": action_result
        })

        # Example 2: System scan flow
        self.logger.log("🖥️ Demo: Running system analysis.")
        system_scan_result = self.threat_agent.analyze_system()

        self.logger.log("🧠 Running Gemini analysis for system scan (if enabled).")
        gemini_system = self.gemini_agent.analyze_system_with_gemini(system_scan_result)
        self.logger.log(
            f"[GeminiAgent] System prioritized actions: "
            f"{gemini_system.get('prioritized_actions') if isinstance(gemini_system, dict) else gemini_system}"
        )

        # Step 1 — Prepare threat info
        system_threat_info = {
            "threat_type": "system_risk",
            "severity": "medium" if system_scan_result.get("system_health") == "AT-RISK" else "low",
            "source": "demo_system_scan",
            "metadata": {"system_scan": system_scan_result}
        }

        # Step 2 — Run actual hardening (create hardening_result FIRST!)
        self.logger.log("🔧 Passing system risk to HardeningExecutor (simulated).")
        hardening_result = self.hardener.apply_hardening({
            "analysis": {"severity": system_threat_info["severity"]}
        })

        # Step 3 — Attach Gemini suggestions AFTER hardening_result is created
        hardening_result["gemini_suggestions"] = gemini_system

        # Step 4 — Save memory
        self.memory.save_hardening({
            "system_threat_info": system_threat_info,
            "hardening_result": hardening_result
        })


        # Final report assembly
        final_report = {
            "file_scan": file_result,
            "file_action": action_result,
            "system_scan": system_scan_result,
            "hardening": hardening_result,
            "memory_snapshot": self.memory.export_memory(),
            "logs": self.logger.get_logs()
        }

        self.logger.log("✅ Demo pipeline finished.")
        return final_report

    # backwards-compatibility: keep run() entry
    def run(self):
        return self.run_demo_pipeline()
