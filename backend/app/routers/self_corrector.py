from fastapi import APIRouter
from pydantic import BaseModel
from app.services.self_corrector import run_self_correction
from app.services.metadata_store import log_event

router = APIRouter(
    prefix="/self",
    tags=["Self Correction"]
)

class SelfFixRequest(BaseModel):
    project_path: str
    max_attempts: int = 3

@router.post("/fix")
def self_fix_endpoint(payload: SelfFixRequest):
    result = run_self_correction(
        project_path=payload.project_path,
        max_attempts=payload.max_attempts
    )
    log_event(
        "self_fix",
        {
            "project_path": payload.project_path,
            "max_attempts": payload.max_attempts,
            "result": result,
        },
    )
    return result
