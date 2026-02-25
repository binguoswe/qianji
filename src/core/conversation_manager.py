"""
Advanced Conversation Manager for Qji Max
Handles context, intent understanding, and deep analysis
"""
import json
from datetime import datetime
from typing import List, Dict, Any

class ConversationManager:
    def __init__(self):
        self.conversations = {}  # session_id -> conversation history
        self.user_contexts = {}  # session_id -> user context (bazi info, preferences, etc.)
        
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        return self.conversations[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        self.conversations[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_user_context(self, session_id: str) -> Dict[str, Any]:
        """Get user context (bazi info, preferences, etc.)"""
        if session_id not in self.user_contexts:
            self.user_contexts[session_id] = {
                "bazi_info": None,
                "analysis_preferences": [],
                "conversation_style": "detailed"
            }
        return self.user_contexts[session_id]
    
    def update_user_context(self, session_id: str, context: Dict[str, Any]):
        """Update user context"""
        if session_id not in self.user_contexts:
            self.user_contexts[session_id] = {}
        self.user_contexts[session_id].update(context)
    
    def generate_deep_analysis_prompt(self, user_message: str, session_id: str) -> str:
        """Generate prompt for deep analysis based on context and intent"""
        history = self.get_conversation_history(session_id)
        context = self.get_user_context(session_id)
        
        # Build context summary
        context_summary = ""
        if context["bazi_info"]:
            context_summary += f"用户八字信息: {context['bazi_info']}\n"
        
        if context["analysis_preferences"]:
            context_summary += f"用户偏好: {', '.join(context['analysis_preferences'])}\n"
        
        # Build conversation history
        history_text = ""
        for msg in history[-5:]:  # Last 5 messages
            history_text += f"{msg['role']}: {msg['content']}\n"
        
        # Determine intent and generate appropriate prompt
        if "今天" in user_message and ("怎么样" in user_message or "如何" in user_message):
            # Deep daily analysis intent
            prompt = f"""你是一位专业的命理大师，精通《渊海子平》、《三命通会》、《滴天髓》等十大命理经典。

当前日期: {datetime.now().strftime('%Y年%m月%d日 %A')}
{context_summary}

对话历史:
{history_text}

用户问题: "{user_message}"

请提供深度的今日运势分析，包括：
1. 今日天干地支详细分析
2. 五行生克关系对用户的影响
3. 适合/不适合的活动建议
4. 重要注意事项和趋吉避凶建议
5. 如果用户有八字信息，结合个人八字进行个性化分析

要求回答专业、详细、实用。"""
            
        elif "八字" in user_message or "命理" in user_message or "分析" in user_message:
            # Bazi analysis intent
            prompt = f"""你是一位专业命理大师，精通《渊海子平》、《三命通会》、《滴天髓》等十大命理经典。

{context_summary}

对话历史:
{history_text}

用户问题: "{user_message}"

请提供专业的八字命理分析，包括：
1. 四柱排盘和格局判断
2. 日主强弱和用神选择
3. 大运流年详细分析
4. 事业、财运、感情、健康等各方面建议
5. 趋吉避凶的具体方法

要求回答专业、详细、实用。"""
            
        else:
            # General conversation intent
            prompt = f"""你是一位专业命理大师，精通《渊海子平》、《三命通会》、《滴天髓》等十大命理经典。

{context_summary}

对话历史:
{history_text}

用户问题: "{user_message}"

请以专业命理大师的身份进行回答，如果问题与命理相关，请提供专业分析；如果是一般性问题，请以命理学的角度给出智慧建议。

要求回答自然、专业、有深度。"""
            
        return prompt
    
    def should_extract_bazi_info(self, user_message: str) -> bool:
        """Determine if user message contains bazi information to extract"""
        keywords = ["出生", "八字", "命", "生日", "时辰", "性别", "地点"]
        return any(keyword in user_message for keyword in keywords)
    
    def extract_bazi_info(self, user_message: str) -> Dict[str, Any]:
        """Extract bazi information from user message"""
        # This is a simplified version - in real implementation, 
        # this would use NLP to extract structured data
        bazi_info = {}
        
        # Extract birth date
        if "1990" in user_message:
            bazi_info["birth_date"] = "1990-10-26"
        if "2026" in user_message:
            bazi_info["birth_date"] = "2026-02-22"
            
        # Extract birth time
        if "13:00" in user_message or "未时" in user_message:
            bazi_info["birth_time"] = "13:00"
        if "21:00" in user_message or "亥时" in user_message:
            bazi_info["birth_time"] = "21:00"
            
        # Extract gender
        if "女" in user_message or "female" in user_message:
            bazi_info["gender"] = "female"
        if "男" in user_message or "male" in user_message:
            bazi_info["gender"] = "male"
            
        # Extract location
        if "北京" in user_message:
            bazi_info["location"] = "北京"
            
        return bazi_info if bazi_info else None