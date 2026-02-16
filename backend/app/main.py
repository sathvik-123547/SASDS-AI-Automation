import logging
import time
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

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
from app.routers.refine import router as refine_router
from app.routers.terminal import router as terminal_router
from app.routers.files import router as files_router
from app.routers.autopilot import router as autopilot_router
from app.routers.chat import router as chat_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("sasds-backend")

app = FastAPI(
    title="SASDS Backend",
    description="AI-powered Single Agent Software Development System",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    if not settings.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set!")
    else:
        logger.info("GEMINI_API_KEY is configured.")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request logging and error handling
@app.middleware("http")
async def log_requests_and_errors(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Error processing {request.method} {request.url.path}: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "exception": str(e)}
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
app.include_router(refine_router)
app.include_router(terminal_router)
app.include_router(files_router)
app.include_router(autopilot_router)
app.include_router(chat_router)
