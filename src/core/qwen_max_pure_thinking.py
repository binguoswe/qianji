"""
Pure Qwen Max Thinking Mode for Qianji AI
Completely relies on Qwen Max's native reasoning and search decision capabilities
No external rules or interventions - let the model think and decide autonomously
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

def call_qwen_max_pure_thinking(prompt, conversation_history=None):
    """
    Call Qwen Max API in pure thinking mode
    
    Let Qwen Max completely decide:
    - Whether to use reasoning/thinking
    - Whether to perform web search  
    - What search strategy to use
    - How to verify information accuracy
    
    No external intervention or rules - pure autonomous AI decision making
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
        
        # Pure thinking mode - let Qwen Max decide everything autonomously
        data = {
            "model": "qwen3-max-2026-01-23",
            "messages": messages,
            "max_tokens": 4096,  # Higher tokens for complex reasoning
            "temperature": 0.7,
            "enable_search": True,  # Enable search capability
            "search_strategy": "auto",  # Let model decide search strategy
            "generationConfig": {
                "extra_body": {
                    "enable_thinking": True  # Enable full reasoning capability
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=120)  # Longer timeout for complex reasoning
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
def test_pure_thinking():
    """Test pure Qwen Max thinking mode"""
    response = call_qwen_max_pure_thinking("请分析今天农历日期，并自主决定是否需要联网验证。")
    return f"Pure thinking test: {response[:200]}..."

if __name__ == "__main__":
    print(test_pure_thinking())