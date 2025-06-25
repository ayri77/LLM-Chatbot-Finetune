"""
API routes for the German Language Teaching Chatbot
"""

import time
import hashlib
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from datetime import datetime

from app.api.schemas import (
    ChatRequest, ChatResponse, ModelStatusResponse, 
    HealthResponse, ErrorResponse, CacheStatsResponse
)
from app.models.model_manager import model_manager
from app.utils.logging import ChatbotLogger
from app.utils.config import get_config

router = APIRouter()
logger = ChatbotLogger("API")

# Performance tracking
start_time = time.time()
cache_stats = {
    "hits": 0,
    "misses": 0,
    "total_requests": 0
}

def get_request_id(request: Request) -> str:
    """Generate a unique request ID"""
    return hashlib.md5(f"{request.url}{time.time()}".encode()).hexdigest()[:8]

@router.post("/chat", response_model=ChatResponse, summary="Chat with the German language tutor")
async def chat_endpoint(
    request: ChatRequest,
    req: Request = Depends(get_request_id)
):
    """
    Chat with the German language teaching chatbot.
    
    - **message**: Your question or request in Russian
    - **max_tokens**: Maximum number of tokens to generate (optional)
    - **temperature**: Sampling temperature (optional)
    - **top_p**: Top-p sampling parameter (optional)
    """
    try:
        request_id = req
        logger.info("Chat request received", 
                   request_id=request_id,
                   message_length=len(request.message),
                   max_tokens=request.max_tokens)
        
        start_time = time.time()
        
        # Generate response
        response = model_manager.chat(request.message, request.max_tokens)
        
        response_time = time.time() - start_time
        
        # Update cache stats (simplified - no actual cache yet)
        cache_stats["total_requests"] += 1
        cache_stats["misses"] += 1  # For now, all are misses
        
        # Count tokens (approximate)
        tokens_generated = len(response.split())
        
        # Get model info
        model_info = {
            "model_loaded": model_manager.model is not None,
            "device": model_manager.device,
            "gpu_memory_gb": model_manager.get_model_status().get("gpu_memory_gb", 0)
        }
        
        logger.info("Chat response generated",
                   request_id=request_id,
                   response_time=response_time,
                   tokens_generated=tokens_generated)
        
        return ChatResponse(
            response=response,
            cached=False,  # No cache implementation yet
            response_time=response_time,
            tokens_generated=tokens_generated,
            model_info=model_info
        )
        
    except Exception as e:
        logger.error("Error in chat endpoint", 
                    request_id=req,
                    error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/model/status", response_model=ModelStatusResponse, summary="Get model status")
async def model_status_endpoint():
    """
    Get the current status of the model including:
    - Model loading status
    - Device information
    - Performance metrics
    - Memory usage
    """
    try:
        status = model_manager.get_model_status()
        return ModelStatusResponse(**status)
        
    except Exception as e:
        logger.error("Error getting model status", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check_endpoint():
    """
    Health check endpoint to verify the service is running properly.
    Returns the current status of the application.
    """
    try:
        uptime = time.time() - start_time
        config = get_config()
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            model_loaded=model_manager.model is not None,
            version=config.get("app.version", "1.0.0"),
            uptime=uptime
        )
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow(),
            model_loaded=False,
            version="1.0.0",
            uptime=time.time() - start_time
        )

@router.get("/ready", summary="Readiness check")
async def readiness_check():
    """
    Readiness check endpoint to verify the service is ready to handle requests.
    """
    try:
        if model_manager.model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        return {"status": "ready", "timestamp": datetime.utcnow()}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service not ready")

@router.get("/live", summary="Liveness check")
async def liveness_check():
    """
    Liveness check endpoint to verify the service is alive.
    """
    return {"status": "alive", "timestamp": datetime.utcnow()}

@router.get("/cache/stats", response_model=CacheStatsResponse, summary="Get cache statistics")
async def cache_stats_endpoint():
    """
    Get cache statistics including hit rate and performance metrics.
    """
    try:
        total_requests = cache_stats["total_requests"]
        hit_rate = cache_stats["hits"] / total_requests if total_requests > 0 else 0.0
        
        return CacheStatsResponse(
            cache_hits=cache_stats["hits"],
            cache_misses=cache_stats["misses"],
            cache_size=0,  # No cache implementation yet
            hit_rate=hit_rate,
            total_requests=total_requests
        )
        
    except Exception as e:
        logger.error("Error getting cache stats", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/cache/clear", summary="Clear cache")
async def clear_cache_endpoint():
    """
    Clear the response cache.
    """
    try:
        # Reset cache stats
        cache_stats["hits"] = 0
        cache_stats["misses"] = 0
        cache_stats["total_requests"] = 0
        
        logger.info("Cache cleared")
        return {"message": "Cache cleared successfully"}
        
    except Exception as e:
        logger.error("Error clearing cache", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/config", summary="Get current configuration")
async def get_config_endpoint():
    """
    Get the current application configuration (without sensitive data).
    """
    try:
        config = get_config()
        
        # Return only non-sensitive configuration
        safe_config = {
            "model": {
                "base_model": config.get("model.base_model"),
                "max_tokens": config.get("model.max_tokens"),
                "temperature": config.get("model.temperature")
            },
            "optimization": {
                "load_in_8bit": config.get("optimization.load_in_8bit"),
                "device_map": config.get("optimization.device_map")
            },
            "api": {
                "host": config.get("api.host"),
                "port": config.get("api.port")
            }
        }
        
        return safe_config
        
    except Exception as e:
        logger.error("Error getting configuration", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    request_id = get_request_id(request)
    
    logger.error("Unhandled exception",
                request_id=request_id,
                error=str(exc),
                path=request.url.path)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            error_type=type(exc).__name__,
            timestamp=datetime.utcnow(),
            request_id=request_id
        ).dict()
    ) 