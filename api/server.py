from fastapi import FastAPI
from routes.action import router as action_router
from routes.file_scan import router as file_scan_router
from routes.system_scan import router as system_scan_router

app = FastAPI(
    title="ThreatGuard AI Security Agent",
    description="API for file scanning, system scanning, and autonomous AI security actions.",
    version="1.0.0"
)

# Register routes
app.include_router(action_router, prefix="/action", tags=["Action Agent"])
app.include_router(file_scan_router, prefix="/file", tags=["File Scanner"])
app.include_router(system_scan_router, prefix="/system", tags=["System Analyzer"])

