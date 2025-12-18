from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, default="")
    status = Column(String, default="active")  # e.g., 'active', 'completed', 'archived'

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")