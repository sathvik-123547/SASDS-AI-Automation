import uuid
from fastapi import APIRouter
from app.schemas.codegen import CodeGenerationResponse
from app.utils.file_writer import write_generated_files

router = APIRouter(
    prefix="/code",
    tags=["Code Writing"]
)

@router.post("/write")
def write_code_to_disk(payload: CodeGenerationResponse):
    """
    Saves the generated project files to disk under:
    generated_projects/{project_id}/
    """
    project_id = f"project_{uuid.uuid4().hex[:8]}"  # unique folder name

    project_path = write_generated_files(
        project_id=project_id,
        files=[file.dict() for file in payload.files]
    )

    return {
        "message": "Project written successfully.",
        "project_id": project_id,
        "project_path": project_path
    }
