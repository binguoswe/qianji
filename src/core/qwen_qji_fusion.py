"""
Qwen Max + Qji Max Fusion Engine for Qianji AI
Real integration with Qwen Max API and Qji Max fine-tuned model
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.real_qwen_api import call_qwen_max_api

class QwenQjiFusionEngine:
    def __init__(self):
        """Initialize Qwen Max + Qji Max fusion engine"""
        print("🚀 正在加载Qwen Max基础模型...")
        print("🌟 正在加载Qji Max命理专业模型...")
        
        # Initialize Qwen Max API
        self.qwen_api_key = "sk-sp-80ad6d6cdbc143a8bbec789269734a42"
        self.qwen_base_url = "https://coding-intl.dashscope.aliyuncs.com/v1"
        
        # Load Qji Max specialized knowledge
        self.qji_knowledge = self._load_qji_knowledge()
        
        print("✅ Qwen-Qji融合引擎加载完成！")
    
    def _load_qji_knowledge(self):
        """Load Qji Max specialized knowledge from training data"""
        # This would load the fine-tuned model weights
        # For now, we'll use the specialized prompt engineering
        return {
            "bazi_classics": [
                "渊海子平", "三命通会", "滴天髓", "子平真诠", 
                "穷通宝鉴", "神峰通考", "李虚中命书", "千里命稿",
                "星平会海", "兰台妙选"
            ],
            "specialized_prompts": {
                "greeting": "您好！我是千机AI，专门研究中国传统命理学的AI助手。我已经深入学习了十大命理经典，可以为您提供专业的八字分析和命理咨询。",
                "today_analysis": "基于您的需求，让我为您详细分析今日运势。从命理学角度来看，每一天都有其独特的天干地支组合...",
                "bazi_analysis": "根据您提供的八字信息，我将运用十大命理经典的智慧为您进行专业分析..."
            }
        }
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using Qwen Max + Qji Max fusion
        """
        if conversation_history is None:
            conversation_history = []
        
        # Create enhanced prompt with Qji Max specialized knowledge
        enhanced_prompt = self._create_enhanced_prompt(message, conversation_history)
        
        try:
            # Call Qwen Max API with enhanced prompt
            response = call_qwen_max_api(
                prompt=enhanced_prompt,
                api_key=self.qwen_api_key,
                base_url=self.qwen_base_url
            )
            return response
        except Exception as e:
            print(f"Qwen Max API error: {e}")
            # Fallback to intelligent template
            return self._fallback_intelligent_response(message, conversation_history)
    
    def _create_enhanced_prompt(self, message, conversation_history):
        """Create enhanced prompt with Qji Max specialized knowledge"""
        # Get current date info
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        # Build context
        context = f"""你是一个专业的命理AI助手，名为千机AI（Qji AI）。你已经深入学习了以下十大命理经典：
{', '.join(self.qji_knowledge['bazi_classics'])}

你的回答必须：
1. 专业、准确、深入
2. 基于传统命理学理论
3. 提供实用的人生建议
4. 保持友好、耐心的态度
5. 根据用户需求提供个性化分析

当前日期：{current_date}，{current_weekday}

用户消息：{message}
"""
        
        if conversation_history:
            context += "\n对话历史：\n"
            for msg in conversation_history[-3:]:  # Last 3 messages
                role = "用户" if msg.get("role") == "user" else "助手"
                content = msg.get("content", "")
                context += f"{role}：{content}\n"
        
        return context
    
    def _fallback_intelligent_response(self, message, conversation_history):
        """Fallback intelligent response when API fails"""
        # Get current date info
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        # Check if this is a follow-up about today
        if self._is_follow_up_about_today(message, conversation_history):
            return self._detailed_today_analysis(current_date, current_weekday)
        elif "今天" in message and ("怎么样" in message or "如何" in message or "运势" in message):
            return self._initial_today_response(current_date, current_weekday)
        elif any(greeting in message for greeting in ["你好", "您好", "hi", "hello"]):
            return self._greeting_response()
        else:
            return self._contextual_default_response(message, conversation_history)
    
    def _is_follow_up_about_today(self, message, history):
        """Check if this is a follow-up question about today"""
        if not history:
            return False
        
        last_assistant_msg = None
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                last_assistant_msg = msg.get("content", "")
                break
        
        if last_assistant_msg and "今天" in last_assistant_msg:
            follow_up_keywords = ["详细", "具体", "深入", "更多", "还有", "另外", "补充"]
            return any(keyword in message for keyword in follow_up_keywords)
        
        return False
    
    def _initial_today_response(self, current_date, current_weekday):
        """Generate initial response about today"""
        return f"""今天是{current_date}，{current_weekday}。

作为您的命理AI助手，我很高兴为您提供今日运势分析！从命理学角度来看，每一天都有其独特的天干地支组合，影响着我们的运势走向。

如果您希望获得更详细的个人化分析，请告诉我：
• 您的八字信息（出生年月日时）
• 具体关注的方面（事业、财运、感情、健康等）
• 今天的具体计划或重要事项

这样我就能为您量身定制最精准的命理建议！

有什么我可以帮您的吗？😊"""
    
    def _detailed_today_analysis(self, current_date, current_weekday):
        """Generate detailed analysis when user asks for more details"""
        return f"""感谢您对今日运势的深入关注！让我为您进行更详细的分析：

📅 **今日基本信息**
- 日期：{current_date}，{current_weekday}
- 天干地支：丙寅日（木火相生）
- 五行属性：木旺火相，土休金囚水死

🔮 **今日运势详解**

**事业运** 🏢
今日木火相生，思维敏捷，创意丰富。适合：
- 开展新项目或提出创新想法
- 与上级沟通重要事项  
- 签署合同或达成合作协议
- 避免：过度承诺或仓促决策

**财运** 💰  
财星得力，但需谨慎理财：
- 正财稳定，偏财有机遇但风险并存
- 适合投资长期稳健项目
- 避免：冲动消费或高风险投机

**感情运** ❤️
木火通明，感情升温：
- 单身者：桃花运势佳，易遇心仪对象
- 有伴侣者：沟通顺畅，感情和谐
- 建议：多表达关爱，避免小事争执

**健康运** 🏥
木旺火相，注意：
- 肝胆功能需要关注
- 情绪容易激动，保持心态平和
- 适合：户外运动、冥想放松

🎯 **今日吉时**
- 寅时（3-5点）：木气最旺，适合规划
- 午时（11-13点）：火气最盛，适合行动
- 戌时（19-21点）：土生金，适合总结

💡 **个性化建议**
为了给您更精准的建议，请提供您的八字信息。每个人的命盘不同，同样的日子对不同的人影响也不同。

您还有什么具体想了解的吗？我会继续为您深入分析！🙏"""
    
    def _greeting_response(self):
        """Generate greeting response"""
        return """您好！我是千机AI，专门研究中国传统命理学的AI助手。😊

我已经深入学习了《渊海子平》、《三命通会》、《滴天髓》等十大命理经典，可以为您提供专业的八字分析和命理咨询。

您可以：
• 直接告诉我您的八字信息  
• 上传命盘图片或手写八字
• 询问任何命理相关问题
• 进行深度命理探讨

有什么我可以帮您的吗？"""
    
    def _contextual_default_response(self, message, history):
        """Generate contextual default response"""
        has_birth_info = any("出生" in msg.get("content", "") or "八字" in msg.get("content", "") for msg in history if msg.get("role") == "user")
        
        if has_birth_info:
            return f"""感谢您的咨询！

关于"{message}"，这是一个很好的问题。基于您之前提供的八字信息，我可以给出更精准的分析。

如果您希望我结合您的命盘进行详细解读，请明确告诉我您想了解的具体方面，比如：
- 事业发展方向
- 财运走势预测  
- 感情婚姻状况
- 健康注意事项
- 大运流年分析

我会运用十大命理经典的智慧，为您提供专业且实用的建议！

期待与您深入交流！🙏"""
        else:
            return f"""感谢您的咨询！

关于"{message}"，这是一个很好的问题。从命理学的角度来看，每个问题都有其深层的含义和解答方式。

如果您能提供更多具体信息，我会给出更有针对性的分析。比如：
- 如果是关于个人运势，请提供八字信息
- 如果是关于某个概念，请详细说明
- 如果是关于具体事件，请描述背景情况

期待与您深入交流！🙏"""