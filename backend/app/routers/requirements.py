from fastapi import APIRouter
from app.schemas.requirements import (
    RequirementAnalysisRequest,
    RequirementAnalysisResponse,
)
from app.services.gemini_client import analyze_requirements_with_gemini

router = APIRouter(
    prefix="/requirements",
    tags=["Requirements Analysis"],
)


@router.post("/analyze", response_model=RequirementAnalysisResponse)
def analyze_requirements(payload: RequirementAnalysisRequest):
    """
    Analyze natural language software requirements and return a structured breakdown.
    """
    result_dict = analyze_requirements_with_gemini(payload.requirements_text)

    # FastAPI + Pydantic will validate this against RequirementAnalysisResponse
    return result_dict
