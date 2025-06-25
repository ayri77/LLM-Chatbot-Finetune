#!/usr/bin/env python3
"""
Startup script for the German Language Teaching Chatbot
"""

import sys
import os
import uvicorn
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def main():
    """Start the chatbot server"""
    print("🚀 Starting German Language Teaching Chatbot...")
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: 'app' directory not found. Please run this script from the chatbot directory.")
        return
    
    # Check if requirements are installed
    try:
        import torch
        import transformers
        import fastapi
        import streamlit
        print("✅ Dependencies check passed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return
    
    # Import and start the application
    try:
        from app.main import app
        from app.utils.config import get_config
        
        # Get configuration
        config = get_config()
        host = config.get("server.host", "0.0.0.0")
        port = config.get("server.port", 8000)
        reload = config.get("server.reload", False)
        workers = config.get("server.workers", 1)
        
        print(f"📡 Server will start on http://{host}:{port}")
        print(f"📚 API documentation will be available at http://{host}:{port}/docs")
        print(f"🔧 Reload mode: {'enabled' if reload else 'disabled'}")
        print(f"👥 Workers: {workers}")
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("Please check the configuration and model files.")

if __name__ == "__main__":
    main() 