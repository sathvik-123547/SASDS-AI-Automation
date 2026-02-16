import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from app.db.base import Base
from enum import Enum as PyEnum

class TaskStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue" # Could be set automatically or manually

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
