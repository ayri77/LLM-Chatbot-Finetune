#!/usr/bin/env python3
"""
Basic test script for the German Language Teaching Chatbot
Tests model loading and basic functionality
"""

import sys
import os
import time

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_config_loading():
    """Test configuration loading"""
    print("🔧 Testing configuration loading...")
    
    try:
        from app.utils.config import get_config
        config = get_config()
        
        print(f"✅ Configuration loaded successfully")
        print(f"   Base model: {config.get('model.base_model')}")
        print(f"   Model path: {config.get('model.model_path')}")
        print(f"   Max tokens: {config.get('model.max_tokens')}")
        print(f"   System prompt: {config.get('system_prompt')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_model_loading():
    """Test model loading"""
    print("\n🤖 Testing model loading...")
    
    try:
        from app.models.model_manager import ModelManager
        
        # Create model manager
        model_mgr = ModelManager()
        
        # Load model
        print("   Loading model (this may take a while)...")
        start_time = time.time()
        
        success = model_mgr.load_model()
        
        load_time = time.time() - start_time
        
        if success:
            print(f"✅ Model loaded successfully in {load_time:.2f}s")
            
            # Get model status
            status = model_mgr.get_model_status()
            print(f"   Device: {status['device']}")
            print(f"   GPU Memory: {status['gpu_memory_gb']:.2f} GB")
            print(f"   Total parameters: {status.get('total_parameters', 'N/A')}")
            
            return True, model_mgr
        else:
            print("❌ Model loading failed")
            return False, None
            
    except Exception as e:
        print(f"❌ Model loading test failed: {e}")
        return False, None

def test_basic_chat(model_mgr):
    """Test basic chat functionality"""
    print("\n💬 Testing basic chat functionality...")
    
    try:
        # Test queries
        test_queries = [
            "Привет! Как дела?",
            "Объясни разницу между wissen и kennen",
            "Создай простое упражнение на тему 'Приветствие'"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   Test {i}: {query}")
            
            start_time = time.time()
            response = model_mgr.chat(query, max_tokens=100)
            response_time = time.time() - start_time
            
            print(f"   Response ({response_time:.2f}s): {response[:100]}...")
            
            if response and "ошибка" not in response.lower():
                print(f"   ✅ Test {i} passed")
            else:
                print(f"   ⚠️ Test {i} returned error response")
        
        return True
        
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def test_api_schemas():
    """Test API schemas"""
    print("\n📋 Testing API schemas...")
    
    try:
        from app.api.schemas import ChatRequest, ChatResponse
        
        # Test ChatRequest
        request = ChatRequest(
            message="Тестовое сообщение",
            max_tokens=256
        )
        print(f"✅ ChatRequest schema works")
        
        # Test ChatResponse
        response = ChatResponse(
            response="Тестовый ответ",
            cached=False,
            response_time=1.5
        )
        print(f"✅ ChatResponse schema works")
        
        return True
        
    except Exception as e:
        print(f"❌ API schemas test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 German Language Teaching Chatbot - Basic Tests")
    print("=" * 50)
    
    # Test configuration
    if not test_config_loading():
        print("\n❌ Configuration test failed. Exiting.")
        return
    
    # Test API schemas
    if not test_api_schemas():
        print("\n❌ API schemas test failed. Exiting.")
        return
    
    # Test model loading
    model_loaded, model_mgr = test_model_loading()
    
    if not model_loaded:
        print("\n❌ Model loading test failed. Exiting.")
        return
    
    # Test basic chat
    if not test_basic_chat(model_mgr):
        print("\n❌ Chat test failed.")
        return
    
    print("\n✅ All basic tests passed!")
    print("\n🎉 The chatbot is ready for deployment!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start the API server: python -m app.main")
    print("3. Access the API docs at: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 