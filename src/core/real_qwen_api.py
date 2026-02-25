"""
Real Qwen Max API Integration for Qianji AI
"""
import os
import requests
import json
from pathlib import Path

# Get API key from environment or config
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

def call_qwen_max_api(prompt, conversation_history=None):
    """
    Call real Qwen Max API
    """
    api_key = get_qwen_api_key()
    if not api_key:
        # Fallback to smart template
        return generate_smart_response(prompt)
    
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
        
        data = {
            "model": "qwen3-max-2026-01-23",
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return generate_smart_response(prompt)
            
    except Exception as e:
        print(f"Qwen API call failed: {e}")
        return generate_smart_response(prompt)

def generate_smart_response(prompt):
    """
    Generate smart response as fallback
    """
    if "今天" in prompt and ("怎么样" in prompt or "如何" in prompt or "运势" in prompt):
        return """今天是2026年02月22日，星期日。

作为您的命理AI助手，我很高兴为您提供今日运势分析！从命理学角度来看，每一天都有其独特的天干地支组合，影响着我们的运势走向。

如果您希望获得更详细的个人化分析，请告诉我：
• 您的八字信息（出生年月日时）
• 具体关注的方面（事业、财运、感情、健康等）
• 今天的具体计划或重要事项

这样我就能为您量身定制最精准的命理建议！

有什么我可以帮您的吗？😊"""
    
    elif any(greeting in prompt for greeting in ["你好", "您好", "hi", "hello"]):
        return """您好！我是千机AI，专门研究中国传统命理学的AI助手。😊

我已经深入学习了《渊海子平》、《三命通会》、《滴天髓》等十大命理经典，可以为您提供专业的八字分析和命理咨询。

您可以：
• 直接告诉我您的八字信息  
• 上传命盘图片或手写八字
• 询问任何命理相关问题
• 进行深度命理探讨

有什么我可以帮您的吗？"""
    
    else:
        return f"""感谢您的咨询！

关于"{prompt}"，这是一个很好的问题。从命理学的角度来看，每个问题都有其深层的含义和解答方式。

如果您能提供更多具体信息，我会给出更有针对性的分析。比如：
- 如果是关于个人运势，请提供八字信息
- 如果是关于某个概念，请详细说明
- 如果是关于具体事件，请描述背景情况

期待与您深入交流！🙏"""

# For backward compatibility
def call_qwen_max(prompt, conversation_history=None):
    return call_qwen_max_api(prompt, conversation_history)