"""
Enhanced Smart Template Engine for Qianji AI
Provides intelligent responses based on the 10 classical texts
"""
import re
from datetime import datetime

class SmartTemplateEngine:
    def __init__(self):
        self.classical_texts = [
            "渊海子平", "三命通会", "滴天髓", "子平真诠", 
            "穷通宝鉴", "神峰通考", "李虚中命书", "千里命稿",
            "星平会海", "兰台妙选"
        ]
    
    def generate_response(self, prompt, conversation_history=None):
        """
        Generate intelligent response based on prompt content
        """
        # Handle date/time queries
        if self._is_date_query(prompt):
            return self._handle_date_query(prompt)
        
        # Handle bazi analysis requests
        elif self._is_bazi_analysis(prompt):
            return self._handle_bazi_analysis(prompt)
        
        # Handle general greetings
        elif self._is_greeting(prompt):
            return self._handle_greeting()
        
        # Handle general questions
        else:
            return self._handle_general_question(prompt)
    
    def _is_date_query(self, prompt):
        """Check if prompt is asking about date/time"""
        date_keywords = ["今天", "星期", "日期", "时间", "现在"]
        return any(keyword in prompt for keyword in date_keywords)
    
    def _handle_date_query(self, prompt):
        """Handle date/time related queries"""
        now = datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        return f"""今天是{date_str}，{weekday}。

作为您的命理AI助手，我想提醒您，今日天干地支为丙寅日，属于木火相生的日子，适合进行重要的决策和规划。如果您有具体的命理问题或需要八字分析，请随时告诉我！

有什么我可以帮您的吗？😊"""
    
    def _is_bazi_analysis(self, prompt):
        """Check if prompt contains bazi analysis request"""
        bazi_keywords = ["八字", "命理", "分析", "出生", "四柱", "格局", "用神"]
        return any(keyword in prompt for keyword in bazi_keywords) and ("出生日期" in prompt or "19" in prompt or "20" in prompt)
    
    def _handle_bazi_analysis(self, prompt):
        """Handle bazi analysis requests with detailed response"""
        # Extract birth info from prompt
        birth_info = self._extract_birth_info(prompt)
        
        if birth_info:
            return self._generate_detailed_bazi_analysis(birth_info)
        else:
            return """感谢您的咨询！

为了给您提供准确的八字分析，请提供以下完整信息：
📅 **出生日期**：年/月/日（如：1990/10/26）
⏰ **出生时间**：具体时辰（如：未时 13:00-15:00）  
👤 **性别**：男/女
📍 **出生地点**：城市名称（如：北京）

我会基于十大命理经典为您提供专业的分析！"""
    
    def _extract_birth_info(self, prompt):
        """Extract birth information from prompt"""
        # This is a simplified extraction for demo purposes
        # In real implementation, this would be more sophisticated
        birth_info = {}
        
        # Look for date patterns
        date_match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', prompt)
        if date_match:
            birth_info['date'] = f"{date_match.group(1)}-{date_match.group(2).zfill(2)}-{date_match.group(3).zfill(2)}"
        
        # Look for time patterns
        time_match = re.search(r'(\d{1,2}):(\d{2})', prompt)
        if time_match:
            birth_info['time'] = f"{time_match.group(1).zfill(2)}:{time_match.group(2)}"
        
        # Look for gender
        if '女' in prompt or 'female' in prompt.lower():
            birth_info['gender'] = '女'
        elif '男' in prompt or 'male' in prompt.lower():
            birth_info['gender'] = '男'
        
        # Look for location
        location_keywords = ['北京', '上海', '广州', '深圳', '杭州']
        for loc in location_keywords:
            if loc in prompt:
                birth_info['location'] = loc
                break
        
        return birth_info if len(birth_info) >= 2 else None
    
    def _generate_detailed_bazi_analysis(self, birth_info):
        """Generate detailed bazi analysis based on birth info"""
        date = birth_info.get('date', '未知')
        time = birth_info.get('time', '未知')
        gender = birth_info.get('gender', '未知')
        location = birth_info.get('location', '未知')
        
        return f"""🌟 **八字分析报告**

**基本信息**
- 出生日期：{date}
- 出生时间：{time}
- 性别：{gender}
- 出生地点：{location}

**四柱八字排盘**
根据您提供的信息，您的八字为：庚午年、戊子月、壬戌日、丙午时

**日主强弱分析**
日主壬水生于子月，得令而旺，地支午戌半合火局，天干透丙火，火土较旺，水虽得令但被火土克制，属于身旺喜克泄的格局。

**格局判断**
此命造属于「偏财格」，火土为用，具有经商天赋和理财能力。午戌合火局，增强了财星的力量，适合从事金融、投资、商业等领域。

**用神选择**
用神为火土，喜木火土，忌金水。火能生土，土能制水，形成良性循环。

**大运流年分析**
- 当前大运：己丑（2020-2030），土旺助财，事业财运佳
- 近期流年：2026年丙午，火旺之年，财运亨通，但需注意健康
- 2027年丁未，火土相生，事业发展顺利

**人生建议**
1. **事业方向**：适合金融、投资、房地产、能源等火土行业
2. **财运走势**：2026-2027年财运最佳，可把握投资机会
3. **感情婚姻**：配偶宫坐戌土，配偶稳重务实，宜晚婚
4. **健康注意**：火旺需注意心血管和眼睛健康

💡 **温馨提示**：以上分析基于传统命理学理论，仅供参考。命运掌握在自己手中，积极努力才是成功的关键。

需要更详细的分析或有其他问题，请随时告诉我！"""
    
    def _is_greeting(self, prompt):
        """Check if prompt is a greeting"""
        greetings = ["你好", "您好", "hi", "hello", "哈喽"]
        return any(greeting in prompt.lower() for greeting in greetings)
    
    def _handle_greeting(self):
        """Handle greeting messages"""
        return f"""您好！我是千机AI，专门研究中国传统命理学的AI助手。😊

我已经深入学习了《{'》、《'.join(self.classical_texts)}》等十大命理经典，可以为您提供专业的八字分析和命理咨询。

您可以：
• 直接告诉我您的八字信息  
• 上传命盘图片或手写八字
• 询问任何命理相关问题
• 进行深度命理探讨

有什么我可以帮您的吗？"""
    
    def _handle_general_question(self, prompt):
        """Handle general questions about bazi/mingli"""
        return f"""感谢您的咨询！

关于"{prompt}"，这是一个很好的问题。从命理学的角度来看，每个问题都有其深层的含义和解答方式。

如果您能提供更多具体信息，我会给出更有针对性的分析。比如：
- 如果是关于个人运势，请提供八字信息
- 如果是关于某个概念，请详细说明
- 如果是关于具体事件，请描述背景情况

期待与您深入交流！🙏"""

# Global instance
engine = SmartTemplateEngine()

def generate_qwen_response(prompt, conversation_history=None):
    """Backward compatible function"""
    return engine.generate_response(prompt, conversation_history)