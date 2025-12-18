from fastapi import APIRouter

from app.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.services.code_reviewer import review_code
from app.services.metadata_store import log_event

router = APIRouter(
    prefix="/review",
    tags=["Code Review"],
)


@router.post("/", response_model=CodeReviewResponse)
def review_code_endpoint(payload: CodeReviewRequest):
    """
    Run AI-assisted code review on provided files.
    """
    files = [file.dict() for file in payload.files]
    result = review_code(payload.requirements_text, files)
    log_event(
        "review",
        {"requirements_text": payload.requirements_text, "files_count": len(files), "result": result},
    )
    return result

