from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from models.todo import Todo, TodoCreate, TodoUpdate

def create_todo(db: Session, todo_create: TodoCreate) -> Todo:
    """
    Creates a new todo item in the database.
    """
    todo_to_db = Todo.model_validate(todo_create)
    db.add(todo_to_db)
    db.commit()
    db.refresh(todo_to_db)
    return todo_to_db

def get_todo(db: Session, todo_id: int) -> Optional[Todo]:
    """
    Retrieves a single todo item by its ID.
    """
    return db.get(Todo, todo_id)

def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
    """
    Retrieves a list of todo items from the database.
    """
    return db.exec(select(Todo).offset(skip).limit(limit)).all()

def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Todo:
    """
    Updates an existing todo item in the database.
    """
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )

    # Use .model_dump(exclude_unset=True) to only update fields that are provided
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    # Update the updated_at timestamp
    db_todo.updated_at = Todo.updated_at.default_factory()

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int) -> dict:
    """
    Deletes a todo item from the database.
    """
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    db.delete(db_todo)
    db.commit()
    return {"message": f"Todo with ID {todo_id} deleted successfully"}

