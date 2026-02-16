from fastapi import APIRouter, HTTPException
from app.schemas.codegen import RefinementRequest, RefinementResponse
from app.services.code_generator import refine_code_with_gemini

router = APIRouter(
    prefix="/refine",
    tags=["Refinement"],
)

@router.post("/", response_model=RefinementResponse)
def refine_code(payload: RefinementRequest):
    """
    Refine a specific file based on natural language instructions.
    """
    result = refine_code_with_gemini(
        path=payload.path,
        content=payload.content,
        instructions=payload.instructions
    )
    return result
