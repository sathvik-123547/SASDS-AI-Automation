from typing import List, Optional
from uuid import UUID, uuid4
from app.schemas import Task, TaskCreate, TaskUpdate
from app.database import tasks_db

def get_all_tasks() -> List[Task]:
    """Retrieves all tasks from the database."""
    return list(tasks_db.values())

def get_task(task_id: UUID) -> Optional[Task]:
    """Retrieves a single task by its ID."""
    return tasks_db.get(task_id)

def create_task(task_create: TaskCreate) -> Task:
    """Creates a new task and adds it to the database."""
    new_task = Task(id=uuid4(), **task_create.model_dump())
    tasks_db[new_task.id] = new_task
    return new_task

def update_task(task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
    """Updates an existing task identified by its ID."""
    if task_id in tasks_db:
        existing_task = tasks_db[task_id]
        # Only update fields that are explicitly provided in the request
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(existing_task, key, value)
        # Re-assign to ensure the dictionary entry is potentially updated (though Pydantic model is mutable)
        tasks_db[task_id] = existing_task
        return existing_task
    return None

def delete_task(task_id: UUID) -> bool:
    """Deletes a task by its ID."""
    if task_id in tasks_db:
        del tasks_db[task_id]
        return True
    return False
