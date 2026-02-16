from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

class Task(Base):
    """
    SQLAlchemy ORM model for a task.
    Represents the 'tasks' table in the database.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
