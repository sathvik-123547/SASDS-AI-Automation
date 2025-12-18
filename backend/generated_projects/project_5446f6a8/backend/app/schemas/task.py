from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in progress"
    done = "done"


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: TaskStatus = TaskStatus.todo


class TaskCreate(TaskBase):
    project_id: int


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[int] = None


class Task(TaskBase):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)