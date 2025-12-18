import os
from pathlib import Path
from typing import Optional

from fastapi import HTTPException

from app.core.config import settings


def sync_project(project_path: str, commit_message: str = "Sync generated project") -> dict:
    """
    Stub GitHub sync. If GITHUB_TOKEN/REPO are not set, returns a no-op response.
    """
    repo = settings.GITHUB_REPO
    token = settings.GITHUB_TOKEN
    branch = settings.GITHUB_BRANCH

    if not repo or not token:
        return {
            "synced": False,
            "reason": "GITHUB_TOKEN or GITHUB_REPO not configured. No action taken.",
        }

    if not Path(project_path).exists():
        raise HTTPException(status_code=400, detail="project_path does not exist.")

    # Real implementation would init repo, commit, and push. We keep a safe stub.
    return {
        "synced": False,
        "reason": "Stub: GitHub sync not executed to avoid side effects.",
        "repo": repo,
        "branch": branch,
        "project_path": os.path.abspath(project_path),
        "commit_message": commit_message,
    }


