"""
Entry point for ThreatGuard.
This script initializes the OrchestratorAgent and runs the demo pipeline.
"""

from agents.orchestrator_agent import OrchestratorAgent

def main():
    orchestrator = OrchestratorAgent()
    report = orchestrator.run()

    # Optional: write final report to file for Kaggle / GitHub evidence
    try:
        import json
        with open("threatguard_run_report.json", "w") as fh:
            json.dump(report, fh, indent=2)
        print("✅ ThreatGuard demo report written to threatguard_run_report.json")
    except Exception as e:
        print("⚠️ Could not write report file:", str(e))

    # Print a short summary to console
    print("\n--- ThreatGuard Demo Summary ---")
    print("File scan detected:", report.get("file_scan", {}).get("detected_issues"))
    print("Action taken:", report.get("file_action", {}).get("action_taken"))
    print("System health:", report.get("system_scan", {}).get("system_health"))
    print("--------------------------------\n")

if __name__ == "__main__":
    main()
