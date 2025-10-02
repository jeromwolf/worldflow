"""
All-Rounder Translation - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api.auth import router as auth_router
from api.projects import router as projects_router

# App initialization
app = FastAPI(
    title="All-Rounder Translation API",
    description="AI-powered PDF translation service (Korean ↔ English)",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
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


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "All-Rounder Translation API",
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
