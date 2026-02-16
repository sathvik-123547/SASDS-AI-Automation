from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import TaskNotFoundException, TaskCreationException, TaskUpdateException, TaskDeletionException
from app.db.init_db import init_db

app = FastAPI(
    title="Simple Task Manager API",
    description="A clean, modular Python backend for managing tasks.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Startup event handler to initialize the database
@app.on_event("startup")
async def startup_event():
    print("Application startup: Initializing database...")
    init_db()

# Custom Exception Handlers
@app.exception_handler(TaskNotFoundException)
async def task_not_found_exception_handler(request: Request, exc: TaskNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(TaskCreationException)
async def task_creation_exception_handler(request: Request, exc: TaskCreationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(TaskUpdateException)
async def task_update_exception_handler(request: Request, exc: TaskUpdateException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(TaskDeletionException)
async def task_deletion_exception_handler(request: Request, exc: TaskDeletionException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_check():
    """
    Checks the health of the API.
    """
    return {"status": "ok", "message": "Task Manager API is running!"}
