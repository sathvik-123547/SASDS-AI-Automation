from typing import Dict
from uuid import UUID
from app.schemas import Task

# In a real application, this would be a connection to a database
# (e.g., SQLAlchemy session, psycopg2 connection).
# For this MVP, we use a simple in-memory dictionary.
tasks_db: Dict[UUID, Task] = {}
