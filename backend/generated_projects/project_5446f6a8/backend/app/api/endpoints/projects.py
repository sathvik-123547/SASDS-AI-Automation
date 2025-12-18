from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.dependencies import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project."""
    return crud.projects.create_project(db=db, project=project)


@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of all projects."""
    projects = crud.projects.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectWithTasks)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific project by its ID, including its tasks."""
    db_project = crud.projects.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    """Update an existing project."""
    db_project = crud.projects.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project and its associated tasks."""
    db_project = crud.projects.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return


@router.get("/{project_id}/tasks", response_model=List[schemas.Task])
def read_project_tasks(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all tasks associated with a specific project ID."""
    # Check if project exists
    project = crud.projects.get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = crud.tasks.get_tasks_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return tasks