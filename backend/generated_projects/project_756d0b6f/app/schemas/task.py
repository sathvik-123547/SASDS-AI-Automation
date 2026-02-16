import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = Field(TaskStatus.PENDING, description="Current status of the task")
    due_date: Optional[datetime.datetime] = Field(None, description="The date the task is due")

class TaskCreate(TaskBase):
    # No additional fields needed for creation beyond TaskBase
    pass

class TaskUpdate(TaskBase):
    # All fields are optional for update
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = Field(None, description="Current status of the task")
    due_date: Optional[datetime.datetime] = Field(None, description="The date the task is due")

class TaskInDB(TaskBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2
