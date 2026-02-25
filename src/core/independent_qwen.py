"""
Independent Qwen Max API Integration for Qianji AI
"""
import os
import requests
import json
from pathlib import Path

# Get API key from OpenClaw config
def get_qwen_api_key():
    try:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config['models']['providers']['bailian']['apiKey']
    except Exception as e:
        print(f"Error loading API key: {e}")
        # Fallback to environment variable
        return os.environ.get('QWEN_API_KEY', 'sk-sp-80ad6d6cdbc143a8bbec789269734a42')

API_KEY = get_qwen_api_key()
BASE_URL = "https://coding-intl.dashscope.aliyuncs.com/v1"

def call_qwen_max_api(prompt, conversation_history=None):
    """
    Call Qwen Max API directly
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
    
    data = {
        "model": "qwen3-max-2026-01-23",
        "messages": messages,
        "max_tokens": 2048,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=60  # Increased timeout to 60 seconds
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return "抱歉，AI服务暂时不可用，请稍后重试。"
            
    except Exception as e:
        print(f"API Exception: {e}")
        return "抱歉，AI服务暂时不可用，请稍后重试。"

# Test function
def test_qwen_api():
    """Test Qwen Max API connection"""
    try:
        response = call_qwen_max_api("你好，这是一个测试。")
        return f"✅ Qwen Max API测试成功: {response[:50]}..."
    except Exception as e:
        return f"❌ Qwen Max API测试失败: {e}"

if __name__ == "__main__":
    print(test_qwen_api())