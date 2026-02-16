from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from core.database import create_db_and_tables
from api.v1.endpoints import todo

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Context manager for application startup and shutdown events.
    Creates database tables on startup.
    """
    print("Application startup: Creating database tables...")
    create_db_and_tables()
    print("Database tables created.")
    yield
    print("Application shutdown: No specific shutdown tasks.")

app = FastAPI(
    title="Todo Application API",
    version="1.0.0",
    description="A simple Todo application backend built with FastAPI and SQLModel.",
    lifespan=lifespan
)

# Include the API routers
app.include_router(todo.router, prefix="/api/v1", tags=["Todos"])

