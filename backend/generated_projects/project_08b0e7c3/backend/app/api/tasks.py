from fastapi import APIRouter, HTTPException, status
from typing import List
from uuid import UUID
from app import crud
from app.schemas import Task, TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Task Management"]
)

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_new_task(task: TaskCreate):
    """
    Create a new task with the provided title, description, and completion status.
    """
    return crud.create_task(task)

@router.get("/", response_model=List[Task], summary="Get all tasks")
def read_all_tasks():
    """
    Retrieve a list of all tasks.
    """
    return crud.get_all_tasks()

@router.get("/{task_id}", response_model=Task, summary="Get a task by ID")
def read_task(task_id: UUID):
    """
    Retrieve a single task by its unique ID.
    """
    task = crud.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@router.put("/{task_id}", response_model=Task, summary="Update an existing task")
def update_existing_task(task_id: UUID, task: TaskUpdate):
    """
    Update an existing task's details.
    Only fields provided in the request body will be updated.
    """
    updated_task = crud.update_task(task_id, task)
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_existing_task(task_id: UUID):
    """
    Delete a task by its unique ID.
    """
    if not crud.delete_task(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return # FastAPI handles 204 No Content response
