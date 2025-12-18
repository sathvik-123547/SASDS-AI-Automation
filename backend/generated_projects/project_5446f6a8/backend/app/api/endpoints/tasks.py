from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.dependencies import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task and associate it with a project."""
    # Ensure the project exists
    project = crud.projects.get_project(db, project_id=task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.tasks.create_task(db=db, task=task)


@router.get("/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of all tasks."""
    tasks = crud.tasks.get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by its ID."""
    db_task = crud.tasks.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task."""
    # If project_id is being updated, ensure the new project exists
    if task.project_id is not None:
        project = crud.projects.get_project(db, project_id=task.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found for task update")

    db_task = crud.tasks.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    db_task = crud.tasks.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return