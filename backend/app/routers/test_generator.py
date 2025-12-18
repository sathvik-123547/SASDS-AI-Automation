from fastapi import APIRouter
from app.schemas.tests import TestGenerationRequest, TestGenerationResponse
from app.services.test_generator import generate_tests
from app.services.metadata_store import log_event

router = APIRouter(
    prefix="/tests",
    tags=["Test Generation"]
)

@router.post("/generate", response_model=TestGenerationResponse)
def generate_tests_endpoint(payload: TestGenerationRequest):
    result = generate_tests(
        requirements_text=payload.requirements_text,
        files=payload.files
    )
    log_event(
        "tests",
        {"requirements_text": payload.requirements_text, "files_count": len(payload.files), "result": result},
    )
    return result
