from fastapi import FastAPI

from backend.app.core.database import create_all_tables
from backend.app.api.endpoints import projects, tasks

app = FastAPI(
    title="Task Manager API",
    description="A simple API for managing projects and tasks.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Create all database tables on application startup."""
    create_all_tables()
    print("Database tables created or already exist.")


app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/", tags=["Root"],
    summary="Health Check",
    description="Checks the health of the API."
)
async def root():
    return {"message": "Welcome to the Task Manager API! Visit /docs for API documentation."}