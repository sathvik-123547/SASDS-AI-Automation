from fastapi import APIRouter
from pydantic import BaseModel

from app.services.github_sync import sync_project

router = APIRouter(
    prefix="/github",
    tags=["GitHub Sync"],
)


class GithubSyncRequest(BaseModel):
    project_path: str
    commit_message: str | None = "Sync generated project"


@router.post("/sync")
def sync_project_endpoint(payload: GithubSyncRequest):
    return sync_project(payload.project_path, payload.commit_message or "Sync generated project")


