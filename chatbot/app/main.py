"""
Main FastAPI application for the German Language Teaching Chatbot
"""

import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api.routes import router
from app.models.model_manager import model_manager
from app.utils.config import get_config
from app.utils.logging import setup_logging, ChatbotLogger

# Setup logging
config = get_config()
setup_logging(
    level=config.get("logging.level", "INFO"),
    log_file=config.get("logging.file"),
    log_format=config.get("logging.format", "json")
)

logger = ChatbotLogger("Main")

# Application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting German Language Teaching Chatbot...")
    
    # Load model
    logger.info("Loading model...")
    if not model_manager.load_model():
        logger.error("Failed to load model during startup")
        raise RuntimeError("Model loading failed")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    model_manager.unload_model()
    logger.info("Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title=config.get("app.name", "German Language Teaching Chatbot"),
    description=config.get("app.description", "AI-powered German language tutor for Russian-speaking students"),
    version=config.get("app.version", "1.0.0"),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get("cors.allow_origins", ["*"]),
    allow_credentials=config.get("cors.allow_credentials", True),
    allow_methods=config.get("cors.allow_methods", ["*"]),
    allow_headers=config.get("cors.allow_headers", ["*"]),
)

# Add trusted host middleware (optional)
trusted_hosts = config.get("server.trusted_hosts")
if trusted_hosts:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=trusted_hosts
    )

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log request
    logger.log_request(
        method=request.method,
        path=str(request.url.path),
        status_code=response.status_code,
        duration=process_time
    )
    
    return response

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["chatbot"])

# Root endpoint
@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint with basic information"""
    return {
        "name": "German Language Teaching Chatbot",
        "version": "1.0.0",
        "description": "AI-powered German language tutor for Russian-speaking students",
        "docs": "/docs",
        "health": "/api/v1/health",
        "model_status": "/api/v1/model/status"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions"""
    logger.error("Unhandled exception",
                error=str(exc),
                path=str(request.url.path),
                method=request.method)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_type": type(exc).__name__,
            "message": "An unexpected error occurred"
        }
    )

# Model-specific exception handler
@app.exception_handler(RuntimeError)
async def model_exception_handler(request: Request, exc: RuntimeError):
    """Handler for model-related runtime errors"""
    logger.error("Model runtime error",
                error=str(exc),
                path=str(request.url.path))
    
    return JSONResponse(
        status_code=503,
        content={
            "error": "Model service unavailable",
            "error_type": "RuntimeError",
            "message": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Get server configuration
    host = config.get("server.host", "0.0.0.0")
    port = config.get("server.port", 8000)
    reload = config.get("server.reload", False)
    workers = config.get("server.workers", 1)
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level="info"
    ) 