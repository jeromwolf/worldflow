"""
All-Rounder Translation - FastAPI Main Application
"""
# DEBUG: Check environment variables at startup
import os
print("="*50)
print("ENVIRONMENT VARIABLES CHECK:")
print(f"DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
print(f"REDIS_URL: {'SET' if os.getenv('REDIS_URL') else 'NOT SET'}")
print(f"OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
print(f"SECRET_KEY: {'SET' if os.getenv('SECRET_KEY') else 'NOT SET'}")
print("="*50)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from api.auth import router as auth_router
from api.projects import router as projects_router
from api.translation import router as translation_router
from api.pdf import router as pdf_router
from core.database import engine, Base
# Import ALL models to ensure they're registered with Base.metadata
from models import (
    User, Project, ProjectImage, Glossary, UsageLog, Payment
)
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup: Create database tables
    logger.info("Creating database tables...")
    logger.debug(f"Tables to create: {list(Base.metadata.tables.keys())}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success(f"Database tables created successfully: {list(Base.metadata.tables.keys())}")

    yield

    # Shutdown
    logger.info("Shutting down...")


# App initialization
app = FastAPI(
    title="WorldFlow API",
    description="AI-powered PDF translation service (Korean ↔ English)",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(translation_router)
app.include_router(pdf_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "WorldFlow API",
        "version": "0.1.0",
        "status": "healthy",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "message": "All systems operational"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
