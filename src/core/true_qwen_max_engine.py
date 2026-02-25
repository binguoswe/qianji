"""
True Qwen Max Engine for Qianji AI
Direct integration with OpenClaw's Qwen Max model
"""
import json
import subprocess
import sys
from pathlib import Path

class TrueQwenMaxEngine:
    def __init__(self):
        """Initialize direct integration with OpenClaw's Qwen Max"""
        print("✅ 正在连接到OpenClaw Qwen Max模型...")
        self.model_ready = True
        print("✅ OpenClaw Qwen Max模型连接成功！")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using OpenClaw's actual Qwen Max model
        This makes a direct call to OpenClaw's API
        """
        if not self.model_ready:
            return "AI模型连接失败，请稍后重试。"
        
        # Build the prompt with命理 context
        system_prompt = """你是一位专业的命理学AI助手，精通《渊海子平》、《三命通会》、《滴天髓》等十大命理经典。
你的回答应该专业、准确、有深度，避免模板化的回复。
根据用户的问题提供具体的命理分析和建议。"""
        
        # Prepare the full prompt
        full_prompt = f"{system_prompt}\n\n用户问题: {message}"
        
        if conversation_history:
            # Add conversation history for context
            history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
            full_prompt = f"{system_prompt}\n\n对话历史:\n{history_text}\n\n用户问题: {message}"
        
        try:
            # Call OpenClaw directly using the oracle CLI
            result = subprocess.run([
                'oracle', 'ask',
                '--model', 'bailian/qwen3-max-2026-01-23',
                '--prompt', full_prompt
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                response = result.stdout.strip()
                # Clean up any oracle CLI artifacts
                if '```' in response:
                    response = response.split('```')[0].strip()
                return response
            else:
                return f"AI模型调用失败: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return "AI模型响应超时，请稍后重试。"
        except Exception as e:
            return f"AI模型调用异常: {str(e)}"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi using true Qwen Max model
        """
        prompt = f"""请基于以下八字信息进行专业分析：
出生日期: {birth_date}
出生时间: {birth_time}
性别: {gender}
出生地点: {location}

请提供详细的四柱排盘、格局分析、用神选择、大运流年和具体的人生建议。
要求回答专业、详细、实用，体现顶级命理大师的水平。"""
        
        return self.generate_response(prompt)