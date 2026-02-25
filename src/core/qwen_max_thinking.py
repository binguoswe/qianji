"""
Qwen Max API with Thinking Mode and Native Web Search
Enables both reasoning (thinking) and web search capabilities
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

def call_qwen_max_thinking(prompt, conversation_history=None, enable_search=True):
    """
    Call Qwen Max API with thinking mode and native web search enabled
    
    This enables both:
    - Reasoning/thinking capability (enable_thinking: true)
    - Native web search (enable_search: true)
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
        
        # Enable both thinking and search
        data = {
            "model": "qwen3-max-2026-01-23",
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7,
            "enable_search": enable_search,
            "search_strategy": "max",
            "generationConfig": {
                "extra_body": {
                    "enable_thinking": True
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=90)  # Longer timeout for thinking
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
def test_qwen_thinking():
    """Test Qwen Max with thinking and search"""
    response = call_qwen_max_thinking("请详细分析今天农历日期，并验证准确性。")
    return f"Qwen Max thinking test: {response[:150]}..."

if __name__ == "__main__":
    print(test_qwen_thinking())