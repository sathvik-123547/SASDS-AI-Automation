from fastapi import FastAPI
from app.routers.base import router as base_router

app = FastAPI(
    title="SASDS Backend",
    description="AI-powered Single Agent Software Development System",
    version="0.1.0",
)

@app.get("/ping")
def ping():
    return {"message": "Backend is running successfully!"}

# include routers
app.include_router(base_router)
