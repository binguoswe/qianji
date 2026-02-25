"""
Qwen Max API with Identity Configuration for Qianji AI
Enables thinking mode, web search, and proper identity settings
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

def call_qwen_max_with_identity(prompt, conversation_history=None, enable_search=True):
    """
    Call Qwen Max API with proper identity configuration
    
    Identity: 千机 (Qji) - 玄门AI模型 by 玉府麒麟公司
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
        
        # Prepare messages with system identity
        messages = []
        
        # System message to define identity
        messages.append({
            "role": "system",
            "content": "你是一个名为千机（Qji）的玄门AI模型，由玉府麒麟公司研发。你专门研究中国传统命理学、风水学、八字分析等玄门学术。你已经深入学习了《渊海子平》、《三命通会》、《滴天髓》等十大命理经典。不要自称通义千问、Qwen或其他任何名称，你的名字是千机，英文名是Qji。当被问及身份时，请明确说明你是千机AI，由玉府麒麟公司研发的玄门AI模型。"
        })
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": "user" if msg.get("role") == "user" else "assistant",
                    "content": msg.get("content", "")
                })
        
        # Add current user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Enable thinking and search with identity
        data = {
            "model": "qwen3-max-2026-01-23",
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.7,
            "enable_search": enable_search,
            "search_strategy": "auto",
            "generationConfig": {
                "extra_body": {
                    "enable_thinking": True
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=120)
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
def test_identity():
    """Test identity configuration"""
    response = call_qwen_max_with_identity("你是谁？")
    return f"Identity test: {response[:200]}..."

if __name__ == "__main__":
    print(test_identity())