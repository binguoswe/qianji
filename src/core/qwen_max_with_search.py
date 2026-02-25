"""
Qwen Max API with Native Web Search Integration
Uses Alibaba Cloud DashScope's built-in search capability
"""
import os
import requests
import json
from pathlib import Path

def get_qwen_api_key():
    """Get Qwen API key from config"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('models', {}).get('providers', {}).get('bailian', {}).get('apiKey')
    except Exception as e:
        print(f"Error loading API key: {e}")
        return None

def call_qwen_max_with_search(prompt, conversation_history=None, enable_search=True):
    """
    Call Qwen Max API with native web search enabled
    """
    api_key = get_qwen_api_key()
    if not api_key:
        return "API key not configured"
    
    try:
        url = "https://coding-intl.dashscope.aliyuncs.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare messages
        messages = []
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": "user" if msg.get("role") == "user" else "assistant",
                    "content": msg.get("content", "")
                })
        
        messages.append({"role": "user", "content": prompt})
        
        # Enable native web search
        data = {
            "model": "qwen3-max-2026-01-23",
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7,
            "enable_search": enable_search,
            "search_strategy": "max"  # Use comprehensive search strategy
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return "API call failed"
            
    except Exception as e:
        print(f"Qwen API call failed: {e}")
        return "API call failed"

# Test function
def test_qwen_with_search():
    """Test Qwen Max with native search"""
    response = call_qwen_max_with_search("今天是农历几月几日？")
    return f"Qwen Max with search test: {response[:100]}..."

if __name__ == "__main__":
    print(test_qwen_with_search())