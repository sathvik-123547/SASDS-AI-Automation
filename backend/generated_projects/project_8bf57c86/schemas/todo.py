# This file is intentionally left minimal for this MVP.
# In a larger project, you might have separate files for request and response schemas
# that are distinct from the SQLModel database models.
# However, for SQLModel, the models themselves often serve as read/create schemas directly
# or with slight modifications as seen in `models/todo.py`.

# Re-exporting from models/todo to make them accessible directly from `schemas.todo`
from models.todo import TodoCreate, TodoRead, TodoUpdate, Todo

