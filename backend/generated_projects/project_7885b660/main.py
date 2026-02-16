from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.database import engine, Base
from api.router import api_router
from core.config import settings
import asyncio # Required for Python 3.10+ create_all sync_run

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the application.
    On startup, it ensures the database tables are created.
    """
    # Startup event: Create database tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown event: Add any cleanup logic here if necessary
    # (e.g., closing external connections)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="A simple task manager API built with FastAPI and SQLAlchemy.",
    lifespan=lifespan
)

# Include the main API router
app.include_router(api_router)

# Example root endpoint (optional)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Task Manager API! Visit /docs for API documentation."}
