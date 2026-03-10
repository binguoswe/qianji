"""
Independent Qwen Max API Integration for Qianji AI with Thinking Mode
"""
import os
import requests
import json
from pathlib import Path

# Get API key from environment variable or .env file
def get_qwen_api_key():
    """Get Qwen API key from environment or .env file"""
    # Try environment variable first
    api_key = os.environ.get('BAILIAN_CODING_PLAN_API_KEY')
    if api_key:
        return api_key
    
    # Try .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.environ.get('BAILIAN_CODING_PLAN_API_KEY')
        if api_key:
            return api_key
    except ImportError:
        pass
    
    # Fallback to hardcoded key (not recommended for production)
    return "sk-sp-80ad6d6cdbc143a8bbec789269734a42"

API_KEY = get_qwen_api_key()
BASE_URL = "https://coding-intl.dashscope.aliyuncs.com/v1"

def call_qwen_max_api(prompt, conversation_history=None):
    """
    Call Qwen Max API with thinking mode enabled
    """
    if conversation_history is None:
        conversation_history = []
    
    # Build messages
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": "user" if msg["role"] == "user" else "assistant",
            "content": msg["content"]
        })
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Enable thinking mode as per the configuration you provided
    data = {
        "model": "qwen3-max-2026-01-23",
        "messages": messages,
        "max_tokens": 2048,
        "temperature": 0.7,
        "extra_body": {
            "enable_thinking": True
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return f"抱歉，AI服务暂时不可用 (错误代码: {response.status_code})，请稍后重试。"
            
    except Exception as e:
        print(f"API Exception: {e}")
        return "抱歉，AI服务暂时不可用，请稍后重试。"

# Test function
def test_qwen_api():
    """Test Qwen Max API connection with thinking mode"""
    try:
        response = call_qwen_max_api("你好，这是一个测试。")
        return f"✅ Qwen Max API (thinking mode) 测试成功: {response[:50]}..."
    except Exception as e:
        return f"❌ Qwen Max API 测试失败: {e}"

if __name__ == "__main__":
    print(test_qwen_api())