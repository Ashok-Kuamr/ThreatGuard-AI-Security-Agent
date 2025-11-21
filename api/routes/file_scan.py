from fastapi import APIRouter
from pydantic import BaseModel

from src.tools.file_scanner import FileScanner

router = APIRouter()

class FileScanRequest(BaseModel):
    file_path: str

@router.post("/scan")
def scan_file(req: FileScanRequest):
    scanner = FileScanner()
    result = scanner.scan_file(req.file_path)
    
    return {
        "message": "File scan completed",
        "input_file": req.file_path,
        "scan_result": result
    }

