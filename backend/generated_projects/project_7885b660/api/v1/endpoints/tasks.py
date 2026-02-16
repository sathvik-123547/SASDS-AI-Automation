from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from core.database import get_db
from repositories.tasks import TaskRepository
from services.tasks import TaskService
from api.v1.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dependency to get TaskRepository
async def get_task_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> TaskRepository:
    """Provides a TaskRepository instance with a database session."""
    return TaskRepository(db)

# Dependency to get TaskService
async def get_task_service(
    task_repo: Annotated[TaskRepository, Depends(get_task_repository)]
) -> TaskService:
    """Provides a TaskService instance with a TaskRepository."""
    return TaskService(task_repo)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """
    Create a new task.
    """
    new_task = await task_service.create_task(task_create)
    return new_task

@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks(
    skip: int = 0,
    limit: int = 100,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """
    Retrieve a list of all tasks.
    """
    tasks = await task_service.get_all_tasks(skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """
    Retrieve a single task by its ID.
    """
    task = await task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """
    Update an existing task.
    """
    updated_task = await task_service.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    """
    Delete a task by its ID.
    """
    deleted_task = await task_service.delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return
