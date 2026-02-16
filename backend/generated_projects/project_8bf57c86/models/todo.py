from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class TodoBase(SQLModel):
    """
    Base model for Todo items, defining common fields.
    Used for creating and updating todos.
    """
    title: str = Field(index=True, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    """
    Database model for a Todo item.
    Inherits from TodoBase and SQLModel (with table=True).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # __tablename__ = "todos" # SQLModel automatically infers table name from class name

    def __repr__(self) -> str:
        return f"Todo(id={self.id}, title='{self.title}', completed={self.completed})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Todo):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class TodoCreate(TodoBase):
    """
    Schema for creating a new Todo item.
    Inherits from TodoBase. ID and timestamps are handled by the database.
    """
    pass


class TodoRead(TodoBase):
    """
    Schema for reading a Todo item (response model).
    Includes the database-generated ID and timestamps.
    """
    id: int
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    """
    Schema for updating an existing Todo item.
    All fields are optional, allowing partial updates.
    """
    title: Optional[str] = Field(default=None, index=True, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)

