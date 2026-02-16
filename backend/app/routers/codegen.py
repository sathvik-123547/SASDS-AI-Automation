from fastapi import APIRouter
from app.schemas.codegen import (
    CodeGenerationRequest,
    CodeGenerationResponse,
)
from app.services.code_generator import generate_code_with_gemini
from app.services.metadata_store import log_event

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

    log_event(
        "codegen",
        {"requirements_text": payload.requirements_text, "analysis": analysis_dict, "result": result},
    )

    return result


from fastapi.responses import StreamingResponse
from app.services.code_generator import generate_code_with_gemini_stream

@router.post("/generate/stream")
def generate_code_stream_endpoint(payload: CodeGenerationRequest):
    """
    Stream generated code as text chunks.
    Format:
    ### FILE: path
    content
    ### END FILE ###
    """
    analysis_dict = payload.analysis.dict() if payload.analysis else None
    
    return StreamingResponse(
        generate_code_with_gemini_stream(
            requirements_text=payload.requirements_text,
            analysis=analysis_dict
        ),
        media_type="text/plain"
    )
