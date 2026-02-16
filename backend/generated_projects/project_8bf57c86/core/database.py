from typing import Generator

from sqlmodel import create_engine, Session

from core.config import settings

# SQLModel base for declarative models
# from sqlmodel import SQLModel (not imported directly here, but implicitly used by models)

engine = create_engine(
    settings.DATABASE_URL,
    echo=True, # Log SQL queries to console
    connect_args={"check_same_thread": False} # Required for SQLite
)

def create_db_and_tables():
    """
    Creates all database tables defined by SQLModel metadata.
    This should be called at application startup.
    """
    from models.todo import Todo # Import all models here to register them with SQLModel metadata
    # from models.user import User # Example for other models
    # This ensures SQLModel.metadata.create_all() knows about all models
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    Yields a session and ensures it's closed after the request.
    """
    with Session(engine) as session:
        yield session

