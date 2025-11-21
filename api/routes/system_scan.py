from fastapi import APIRouter
from src.tools.system_analyzer import SystemAnalyzer

router = APIRouter()

@router.get("/health")
def system_health():
    analyzer = SystemAnalyzer()
    result = analyzer.analyze()

    return {
        "message": "System health scan completed",
        "system_status": result
    }

