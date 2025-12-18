from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.base import router as base_router
from app.routers.requirements import router as requirements_router
from app.routers.codegen import router as codegen_router
from app.routers.code_writer import router as code_writer_router
from app.routers.test_generator import router as tests_router
from app.routers.self_corrector import router as self_fix_router
from app.routers.review import router as review_router
from app.routers.github_sync import router as github_router
from app.routers.projects import router as projects_router
from app.routers.runs import router as runs_router


app = FastAPI(
    title="SASDS Backend",
    description="AI-powered Single Agent Software Development System",
    version="0.1.0",
)

# Allow local dev frontends (adjust origins if you deploy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "Backend is running successfully!"}

# Include routers
app.include_router(base_router)
app.include_router(requirements_router)
app.include_router(codegen_router)
app.include_router(code_writer_router)
app.include_router(tests_router)
app.include_router(self_fix_router)
app.include_router(review_router)
app.include_router(github_router)
app.include_router(projects_router)
app.include_router(runs_router)

