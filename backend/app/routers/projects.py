import shutil
import tempfile
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

BASE_DIR = Path("generated_projects")

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get("/")
def list_projects():
    """
    List generated projects under generated_projects/.
    """
    projects = []
    if BASE_DIR.exists():
        for entry in sorted(BASE_DIR.iterdir()):
            if entry.is_dir():
                stat = entry.stat()
                projects.append(
                    {
                        "project_id": entry.name,
                        "project_path": str(entry.resolve()),
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    }
                )

    return {"projects": projects}


@router.get("/{project_id}/download")
def download_project(project_id: str):
    """
    Zip a generated project folder and return it as a download.
    """
    project_dir = BASE_DIR / project_id
    if not project_dir.exists() or not project_dir.is_dir():
        raise HTTPException(status_code=404, detail="Project not found.")

    # Create a temporary zip archive
    tmp_dir = Path(tempfile.gettempdir())
    archive_base = tmp_dir / f"{project_id}_archive"
    archive_path = shutil.make_archive(str(archive_base), "zip", root_dir=project_dir)

    filename = f"{project_id}.zip"
    return FileResponse(
        archive_path,
        media_type="application/zip",
        filename=filename,
    )


