from repositories.tasks import TaskRepository
from api.v1.schemas.tasks import TaskCreate, TaskUpdate
from models.tasks import Task
from typing import List, Optional

class TaskService:
    """
    Business logic layer for Task operations.
    Orchestrates repository interactions and applies business rules.
    """
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def create_task(self, task_create: TaskCreate) -> Task:
        """
        Creates a new task.
        Additional business logic (e.g., permission checks, default values) could go here.
        """
        task_data = task_create.model_dump()
        return await self.task_repo.create(task_data)

    async def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Retrieves all tasks.
        """
        return await self.task_repo.get_all(skip=skip, limit=limit)

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a task by its ID.
        """
        return await self.task_repo.get_by_id(task_id)

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """
        Updates an existing task.
        Applies updates only for fields that are explicitly provided.
        """
        # model_dump(exclude_unset=True) ensures only provided fields are updated
        task_data = task_update.model_dump(exclude_unset=True)
        return await self.task_repo.update(task_id, task_data)

    async def delete_task(self, task_id: int) -> Optional[Task]:
        """
        Deletes a task.
        """
        return await self.task_repo.delete(task_id)
