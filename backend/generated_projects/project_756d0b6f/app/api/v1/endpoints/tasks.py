from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskInDB
from app.services.task_service import TaskService

router = APIRouter()

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency to provide a TaskService instance."""
    return TaskService(db)

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED, summary="Create a new task")
async def create_task(task: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    """
    Creates a new task with the provided details.
    """
    return task_service.create_task(task)

@router.get("/", response_model=List[TaskInDB], summary="Get all tasks")
async def get_all_tasks(task_service: TaskService = Depends(get_task_service)):
    """
    Retrieves a list of all tasks in the system.
    """
    return task_service.get_all_tasks()

@router.get("/{task_id}", response_model=TaskInDB, summary="Get task by ID")
async def get_task_by_id(task_id: int, task_service: TaskService = Depends(get_task_service)):
    """
    Retrieves a specific task by its unique identifier.
    """
    return task_service.get_task_by_id(task_id)

@router.put("/{task_id}", response_model=TaskInDB, summary="Update an existing task")
async def update_task(task_id: int, task: TaskUpdate, task_service: TaskService = Depends(get_task_service)):
    """
    Updates an existing task identified by its unique identifier.
    """
    return task_service.update_task(task_id, task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
async def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    """
    Deletes a task from the system by its unique identifier.
    """
    task_service.delete_task(task_id)
    return
