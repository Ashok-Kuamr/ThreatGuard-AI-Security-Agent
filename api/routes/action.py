from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from src.agents.orchestrator_agent import OrchestratorAgent

app = FastAPI(title="ThreatGuard AI Security Agent API")

class ScanRequest(BaseModel):
    mode: str = "full"   # can be extended later

@app.post("/run")
def run_threatguard(req: ScanRequest):
    orchestrator = OrchestratorAgent()
    result = orchestrator.run()
    return {
        "message": "ThreatGuard executed successfully",
        "mode_used": req.mode,
        "report": result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

