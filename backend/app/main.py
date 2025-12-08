from fastapi import FastAPI
from app.routers.base import router as base_router
from app.routers.requirements import router as requirements_router
from app.routers.codegen import router as codegen_router 
from app.routers.code_writer import router as code_writer_router
from app.routers.test_generator import router as tests_router
from app.routers.self_corrector import router as self_fix_router


app = FastAPI(
    title="SASDS Backend",
    description="AI-powered Single Agent Software Development System",
    version="0.1.0",
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

