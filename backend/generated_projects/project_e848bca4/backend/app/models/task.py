from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    status: str = Field("pending", max_length=50) # e.g., "pending", "completed", "in progress"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    # Make fields optional for updates, so only provided fields are changed
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=50)

class TaskInDB(TaskBase):
    id: int

    class Config:
        from_attributes = True