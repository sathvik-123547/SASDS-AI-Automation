from fastapi import FastAPI
from app.api.v1.endpoints import calculator

app = FastAPI(
    title="Basic Calculator API",
    description="A simple calculator application built with FastAPI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(calculator.router, prefix="/api/v1", tags=["Calculator"])

