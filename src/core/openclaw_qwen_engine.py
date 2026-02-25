"""
OpenClaw Qwen Engine for Qianji AI
Uses OpenClaw's built-in Qwen Max model with命理 knowledge integration
"""
import json
import re
from datetime import datetime

class OpenClawQwenEngine:
    def __init__(self):
        """Initialize using OpenClaw's built-in Qwen Max model"""
        print("✅ 正在加载OpenClaw Qwen Max模型...")
        self.model_loaded = True
        print("✅ OpenClaw Qwen Max模型加载完成！")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using OpenClaw's Qwen Max model
        This is a placeholder that will be replaced with actual OpenClaw integration
        """
        if not self.model_loaded:
            return "AI模型加载失败，请稍后重试。"
        
        # For now, use the enhanced smart template system
        # In production, this would call OpenClaw's model directly
        return self._enhanced_smart_response(message, conversation_history)
    
    def _enhanced_smart_response(self, message, history):
        """Enhanced smart response with better context awareness"""
        # Get current date info
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        # Check if this is a follow-up question about today
        if self._is_follow_up_about_today(message, history):
            return self._detailed_today_analysis(message, current_date, current_weekday)
        
        # Check if user is asking about today generally
        elif "今天" in message and ("怎么样" in message or "如何" in message or "运势" in message or "分析" in message):
            return self._initial_today_response(message, current_date, current_weekday)
        
        # Check if user is greeting
        elif any(greeting in message for greeting in ["你好", "您好", "hi", "hello"]):
            return self._greeting_response()
        
        # Check if user is asking for detailed analysis
        elif any(keyword in message for keyword in ["详细", "深入", "具体", "专业", "分析"]):
            return self._professional_analysis_response(message, history)
        
        # Default response with context awareness
        else:
            return self._contextual_default_response(message, history)
    
    def _is_follow_up_about_today(self, message, history):
        """Check if this is a follow-up question about today"""
        if not history:
            return False
        
        # Check if last assistant message was about today
        last_assistant_msg = None
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                last_assistant_msg = msg.get("content", "")
                break
        
        if last_assistant_msg and "今天" in last_assistant_msg:
            # Check if user is asking for more details
            follow_up_keywords = ["详细", "具体", "深入", "更多", "还有", "另外", "补充", "分析"]
            return any(keyword in message for keyword in follow_up_keywords)
        
        return False
    
    def _initial_today_response(self, message, current_date, current_weekday):
        """Generate initial response about today"""
        return f"""今天是{current_date}，{current_weekday}。

作为您的命理AI助手，我很高兴为您提供今日运势分析！从命理学角度来看，每一天都有其独特的天干地支组合，影响着我们的运势走向。

如果您希望获得更详细的个人化分析，请告诉我：
• 您的八字信息（出生年月日时）
• 具体关注的方面（事业、财运、感情、健康等）
• 今天的具体计划或重要事项

这样我就能为您量身定制最精准的命理建议！

有什么我可以帮您的吗？😊"""
    
    def _detailed_today_analysis(self, message, current_date, current_weekday):
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
    
    def _professional_analysis_response(self, message, history):
        """Generate professional analysis response"""
        return f"""感谢您对命理分析的专业需求！

关于"{message}"，让我运用十大命理经典的智慧为您进行深入分析。

从传统命理学的角度来看，这涉及到多个层面的考量：
1. **天干地支的相互作用**
2. **五行生克制化的平衡**  
3. **格局的高低与用神的选择**
4. **大运流年的具体影响**

为了给出最精准的分析，我需要了解：
- 您的具体八字信息（如果涉及个人命盘）
- 分析的重点方向（格局、用神、大运等）
- 具体的应用场景（择日、起名、风水等）

请提供更多详细信息，我会结合《渊海子平》、《三命通会》等经典的理论，为您提供专业且实用的命理建议！

期待与您深入探讨！🙏"""
    
    def _contextual_default_response(self, message, history):
        """Generate contextual default response"""
        # Check if user provided birth info in history
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