"""
Pydantic schemas for the German Language Teaching Chatbot API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(..., description="User message", min_length=1, max_length=1000)
    max_tokens: Optional[int] = Field(256, description="Maximum tokens to generate", ge=1, le=1000)
    temperature: Optional[float] = Field(0.2, description="Sampling temperature", ge=0.0, le=2.0)
    top_p: Optional[float] = Field(0.9, description="Top-p sampling", ge=0.0, le=1.0)
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Объясни разницу между wissen и kennen на A2 уровне",
                "max_tokens": 256,
                "temperature": 0.2,
                "top_p": 0.9
            }
        }

class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    response: str = Field(..., description="Generated response")
    cached: bool = Field(False, description="Whether response was served from cache")
    response_time: float = Field(..., description="Response generation time in seconds")
    tokens_generated: Optional[int] = Field(None, description="Number of tokens generated")
    model_info: Optional[Dict[str, Any]] = Field(None, description="Model information")
    
    class Config:
        schema_extra = {
            "example": {
                "response": "Wissen и kennen - это два немецких глагола, которые переводятся как 'знать'...",
                "cached": False,
                "response_time": 2.5,
                "tokens_generated": 45,
                "model_info": {
                    "model_loaded": True,
                    "device": "cuda",
                    "gpu_memory_gb": 3.2
                }
            }
        }

class ModelStatusResponse(BaseModel):
    """Response schema for model status endpoint"""
    model_loaded: bool = Field(..., description="Whether model is loaded")
    tokenizer_loaded: bool = Field(..., description="Whether tokenizer is loaded")
    device: str = Field(..., description="Device being used (cuda/cpu)")
    load_time: float = Field(..., description="Model load time in seconds")
    total_inferences: int = Field(..., description="Total number of inferences")
    total_tokens_generated: int = Field(..., description="Total tokens generated")
    gpu_memory_gb: float = Field(..., description="GPU memory usage in GB")
    system_prompt: str = Field(..., description="System prompt being used")
    
    class Config:
        schema_extra = {
            "example": {
                "model_loaded": True,
                "tokenizer_loaded": True,
                "device": "cuda",
                "load_time": 15.2,
                "total_inferences": 42,
                "total_tokens_generated": 1250,
                "gpu_memory_gb": 3.2,
                "system_prompt": "Ты — преподаватель немецкого языка для русскоязычных студентов уровня A2..."
            }
        }

class HealthResponse(BaseModel):
    """Response schema for health check endpoint"""
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Current timestamp")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    version: str = Field(..., description="Application version")
    uptime: Optional[float] = Field(None, description="Application uptime in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "model_loaded": True,
                "version": "1.0.0",
                "uptime": 3600.5
            }
        }

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Error type")
    timestamp: datetime = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Model not loaded",
                "error_type": "RuntimeError",
                "timestamp": "2024-01-15T10:30:00Z",
                "request_id": "req_123456"
            }
        }

class CacheStatsResponse(BaseModel):
    """Response schema for cache statistics"""
    cache_hits: int = Field(..., description="Number of cache hits")
    cache_misses: int = Field(..., description="Number of cache misses")
    cache_size: int = Field(..., description="Current cache size")
    hit_rate: float = Field(..., description="Cache hit rate")
    total_requests: int = Field(..., description="Total requests")
    
    class Config:
        schema_extra = {
            "example": {
                "cache_hits": 25,
                "cache_misses": 75,
                "cache_size": 100,
                "hit_rate": 0.25,
                "total_requests": 100
            }
        } 