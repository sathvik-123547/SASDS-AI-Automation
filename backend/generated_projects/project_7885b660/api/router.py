from fastapi import APIRouter
from api.v1.endpoints import tasks as tasks_v1

# Main API router for versioning and aggregation
api_router = APIRouter(prefix="/api")

# Include v1 API routers
api_router.include_router(tasks_v1.router, prefix="/v1")
