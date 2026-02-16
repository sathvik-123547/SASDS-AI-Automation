from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.exceptions import TaskNotFoundException, TaskCreationException, TaskUpdateException, TaskDeletionException

class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_create: TaskCreate) -> Task:
        try:
            db_task = Task(**task_create.model_dump())
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except Exception as e:
            self.db.rollback()
            raise TaskCreationException(detail=f"Database error: {e}")

    def get_all_tasks(self) -> List[Task]:
        return self.db.query(Task).all()

    def get_task_by_id(self, task_id: int) -> Task:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        db_task = self.get_task_by_id(task_id) # This will raise TaskNotFoundException if not found

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        try:
            self.db.add(db_task) # Not strictly needed if object is already tracked by session
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except Exception as e:
            self.db.rollback()
            raise TaskUpdateException(task_id=task_id, detail=f"Database error: {e}")

    def delete_task(self, task_id: int) -> dict:
        db_task = self.get_task_by_id(task_id) # This will raise TaskNotFoundException if not found
        try:
            self.db.delete(db_task)
            self.db.commit()
            return {"message": f"Task with ID {task_id} deleted successfully."}
        except Exception as e:
            self.db.rollback()
            raise TaskDeletionException(task_id=task_id, detail=f"Database error: {e}")
