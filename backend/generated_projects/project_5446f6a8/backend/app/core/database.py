from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.app.core.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# For SQLite, connect_args is needed for multiple threads
# if not using an in-memory database.
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_all_tables():
    Base.metadata.create_all(bind=engine)