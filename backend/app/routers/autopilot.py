from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from app.services.auto_pilot import analyze_project_structure

router = APIRouter(
    prefix="/autopilot",
    tags=["Auto-Pilot"]
)

class AutoPilotRequest(BaseModel):
    project_id: str

@router.post("/analyze")
def analyze_project(payload: AutoPilotRequest) -> Dict[str, Any]:
    """
    Analyzes the project structure and content using Gemini.
    Returns suggestions and issues.
    """
    result = analyze_project_structure(payload.project_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
