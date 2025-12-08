from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class TaskBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, eggs, bread, cheese")
    completed: bool = Field(False, example=False)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, example="Buy groceries")
    description: Optional[str] = Field(None, example="Milk, eggs, bread, cheese")
    completed: Optional[bool] = Field(None, example=True)

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4, example="123e4567-e89b-12d3-a456-426614174000")
    title: str = Field(..., example="Go to the gym")
    description: Optional[str] = Field(None, example="Workout for an hour")
    completed: bool = Field(False, example=False)

    class Config:
        from_attributes = True # Enable ORM mode for Pydantic v2
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Go to the gym",
                "description": "Workout for an hour",
                "completed": False
            }
        }
