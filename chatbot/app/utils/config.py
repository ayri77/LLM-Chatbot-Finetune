"""
Configuration management for the German Language Teaching Chatbot
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Configuration manager for the chatbot application"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML files"""
        try:
            # Load model configuration
            model_config_path = self.config_dir / "model_config.yaml"
            if model_config_path.exists():
                with open(model_config_path, 'r', encoding='utf-8') as f:
                    self._config.update(yaml.safe_load(f))
            
            # Load app configuration
            app_config_path = self.config_dir / "app_config.yaml"
            if app_config_path.exists():
                with open(app_config_path, 'r', encoding='utf-8') as f:
                    self._config.update(yaml.safe_load(f))
            
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Set default configuration
            self._set_default_config()
    
    def _set_default_config(self):
        """Set default configuration if loading fails"""
        self._config = {
            "model": {
                "base_model": "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
                "model_path": "../models/checkpoint-3",
                "max_tokens": 256,
                "temperature": 0.2,
                "do_sample": False
            },
            "optimization": {
                "load_in_8bit": True,
                "device_map": "auto",
                "torch_dtype": "float16"
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000
            },
            "cache": {
                "redis_url": "redis://localhost:6379",
                "ttl": 3600
            }
        }
        logger.warning("Using default configuration")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration"""
        return self._config.get("model", {})
    
    def get_optimization_config(self) -> Dict[str, Any]:
        """Get optimization configuration"""
        return self._config.get("optimization", {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self._config.get("api", {})
    
    def get_cache_config(self) -> Dict[str, Any]:
        """Get cache configuration"""
        return self._config.get("cache", {})
    
    def get_system_prompt(self) -> str:
        """Get system prompt"""
        prompt = self._config.get("system_prompt")
        if isinstance(prompt, str):
            return prompt
        return "Ты — преподаватель немецкого языка для русскоязычных студентов уровня A2. Объясняй грамотно, понятно, без лишней воды."
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.info(f"Configuration updated: {key} = {value}")

# Global configuration instance
config_manager = ConfigManager()

def load_config() -> Dict[str, Any]:
    """Load configuration and return as dictionary"""
    return config_manager._config

def get_config() -> ConfigManager:
    """Get configuration manager instance"""
    return config_manager 