from fastapi import APIRouter
from app.schemas.codegen import (
    CodeGenerationRequest,
    CodeGenerationResponse,
)
from app.services.code_generator import generate_code_with_gemini

router = APIRouter(
    prefix="/code",
    tags=["Code Generation"],
)


@router.post("/generate", response_model=CodeGenerationResponse)
def generate_code_endpoint(payload: CodeGenerationRequest):
    """
    Generate project code files based on the requirements and optional analysis.
    """
    analysis_dict = payload.analysis.dict() if payload.analysis else None

    result = generate_code_with_gemini(
        requirements_text=payload.requirements_text,
        analysis=analysis_dict,
    )

    return result
