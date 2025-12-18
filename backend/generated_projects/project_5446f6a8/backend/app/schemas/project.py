from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    status: ProjectStatus = ProjectStatus.active


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    status: Optional[ProjectStatus] = None


class Project(ProjectBase):
    id: int
    status: ProjectStatus

    model_config = ConfigDict(from_attributes=True)


# Schema for relationship - to be used when embedding Tasks in Project response, for example
class ProjectWithTasks(Project):
    from .task import Task  # Avoid circular import
    tasks: list[Task] = []