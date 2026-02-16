from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from core.database import get_db
from schemas.todo import TodoCreate, TodoRead, TodoUpdate
from crud import todo as crud_todo # Alias crud.todo to avoid name collision with schemas.todo

router = APIRouter()

@router.post("/todos/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_new_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Creates a new todo item.
    """
    return crud_todo.create_todo(db=db, todo_create=todo)

@router.get("/todos/", response_model=List[TodoRead])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all todo items.
    """
    todos = crud_todo.get_todos(db=db, skip=skip, limit=limit)
    return todos

@router.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single todo item by its ID.
    """
    todo = crud_todo.get_todo(db=db, todo_id=todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {todo_id} not found"
        )
    return todo

@router.put("/todos/{todo_id}", response_model=TodoRead)
def update_existing_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing todo item by its ID.
    """
    try:
        updated_todo = crud_todo.update_todo(db=db, todo_id=todo_id, todo_update=todo)
        return updated_todo
    except HTTPException as e:
        raise e

@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_existing_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Deletes a todo item by its ID.
    """
    try:
        return crud_todo.delete_todo(db=db, todo_id=todo_id)
    except HTTPException as e:
        raise e
