from fastapi import FastAPI
from backend.app.api.v1 import task

app = FastAPI(
    title="Simple Task API",
    description="A FastAPI backend for basic CRUD operations on tasks.",
    version="1.0.0"
)

app.include_router(task.router, prefix="/api/v1/tasks", tags=["tasks"])

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Simple Task API! Visit /docs for API documentation."}