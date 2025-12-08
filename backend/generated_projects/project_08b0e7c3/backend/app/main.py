from fastapi import FastAPI
from app.api import tasks

app = FastAPI(
    title="Todo List API",
    description="A simple REST API for managing todo tasks.",
    version="0.1.0",
    docs_url="/", # Serve OpenAPI docs at the root URL
    redoc_url=None # Disable Redoc
)

# Include the tasks router to register its endpoints with the main app
app.include_router(tasks.router)

@app.get("/health", tags=["Monitoring"], summary="Health check endpoint")
async def health_check():
    """A simple health check endpoint to verify the API is running."""
    return {"status": "ok"}
