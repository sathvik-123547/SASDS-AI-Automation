from fastapi import APIRouter, HTTPException, status
from typing import List

from backend.app.models.task import TaskCreate, TaskUpdate, TaskInDB
from backend.app.crud import task as crud_task

router = APIRouter()

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate):
    """
    Create a new task.
    """
    return crud_task.create_task(task)

@router.get("/", response_model=List[TaskInDB])
def read_all_tasks():
    """
    Retrieve a list of all tasks.
    """
    return crud_task.get_all_tasks()

@router.get("/{task_id}", response_model=TaskInDB)
def read_task(task_id: int):
    """
    Retrieve a single task by its unique identifier.
    """
    task = crud_task.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskInDB)
def update_existing_task(task_id: int, task: TaskUpdate):
    """
    Update an existing task by its unique identifier.
    """
    updated_task = crud_task.update_task(task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: int):
    """
    Delete a task by its unique identifier.
    """
    deleted_task = crud_task.delete_task(task_id)
    if deleted_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # FastAPI automatically handles 204 No Content for routes returning None