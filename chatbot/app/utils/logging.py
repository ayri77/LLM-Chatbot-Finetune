"""
Logging configuration for the German Language Teaching Chatbot
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import structlog
from datetime import datetime

def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "json"
) -> None:
    """
    Setup logging configuration for the chatbot application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_format: Log format (json or text)
    """
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog for structured logging
    if log_format == "json":
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    
    # Configure standard logging
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    if log_format == "json":
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("transformers").setLevel(logging.WARNING)
    logging.getLogger("torch").setLevel(logging.WARNING)
    
    logging.info(f"Logging configured - Level: {level}, Format: {log_format}")

def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)

class ChatbotLogger:
    """Custom logger for chatbot-specific logging"""
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
        self.name = name
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, **kwargs)
    
    def log_request(self, method: str, path: str, status_code: int, duration: float):
        """Log HTTP request"""
        self.logger.info(
            "HTTP Request",
            method=method,
            path=path,
            status_code=status_code,
            duration=duration
        )
    
    def log_model_inference(self, prompt_length: int, response_length: int, duration: float):
        """Log model inference"""
        self.logger.info(
            "Model Inference",
            prompt_length=prompt_length,
            response_length=response_length,
            duration=duration
        )
    
    def log_cache_hit(self, cache_key: str):
        """Log cache hit"""
        self.logger.info("Cache Hit", cache_key=cache_key)
    
    def log_cache_miss(self, cache_key: str):
        """Log cache miss"""
        self.logger.info("Cache Miss", cache_key=cache_key)
    
    def log_error(self, error: Exception, context: str = ""):
        """Log error with context"""
        self.logger.error(
            "Error occurred",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context
        ) 