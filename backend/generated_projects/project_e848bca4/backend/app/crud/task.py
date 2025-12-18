from typing import List, Dict, Optional
from backend.app.models.task import TaskCreate, TaskUpdate, TaskInDB

# In-memory database simulation
tasks_db: Dict[int, TaskInDB] = {}
next_id: int = 1

def get_all_tasks() -> List[TaskInDB]:
    """Retrieves all tasks from the in-memory store."""
    return list(tasks_db.values())

def get_task(task_id: int) -> Optional[TaskInDB]:
    """Retrieves a single task by its ID."""
    return tasks_db.get(task_id)

def create_task(task: TaskCreate) -> TaskInDB:
    """Creates a new task and adds it to the in-memory store."""
    global next_id
    db_task = TaskInDB(id=next_id, **task.model_dump())
    tasks_db[next_id] = db_task
    next_id += 1
    return db_task

def update_task(task_id: int, task_update: TaskUpdate) -> Optional[TaskInDB]:
    """Updates an existing task by its ID with the provided data."""
    existing_task = tasks_db.get(task_id)
    if existing_task:
        update_data = task_update.model_dump(exclude_unset=True)
        updated_task_data = existing_task.model_dump()
        updated_task_data.update(update_data)
        updated_task = TaskInDB(**updated_task_data)
        tasks_db[task_id] = updated_task
        return updated_task
    return None

def delete_task(task_id: int) -> Optional[TaskInDB]:
    """Deletes a task by its ID from the in-memory store."""
    return tasks_db.pop(task_id, None)