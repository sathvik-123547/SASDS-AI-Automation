from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.tasks import Task
from typing import List, Dict, Any, Optional

class TaskRepository:
    """
    Data access layer for Task operations.
    Handles direct interaction with the database using SQLAlchemy ORM.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_data: Dict[str, Any]) -> Task:
        """
        Creates a new task in the database.
        """
        db_task = Task(**task_data)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Retrieves all tasks from the database with pagination.
        """
        result = await self.db.execute(select(Task).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieves a single task by its ID.
        """
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalars().first()

    async def update(self, task_id: int, task_data: Dict[str, Any]) -> Optional[Task]:
        """
        Updates an existing task by its ID with the given data.
        Returns the updated task or None if not found.
        """
        stmt = update(Task).where(Task.id == task_id).values(**task_data).returning(Task)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    async def delete(self, task_id: int) -> Optional[Task]:
        """
        Deletes a task by its ID.
        Returns the deleted task or None if not found.
        """
        stmt = delete(Task).where(Task.id == task_id).returning(Task)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()
