"""
Final Qji Max Engine with Smart Routing and Thinking Mode
Combines accurate date handling with Qwen Max thinking capabilities
"""
from .smart_router import SmartRouter

class IndependentQjiFinalEngine:
    def __init__(self):
        """Initialize final Qji Max engine with smart routing"""
        print("🚀 正在初始化最终版Qji Max引擎（智能路由+Thinking模式）...")
        self.smart_router = SmartRouter()
        print("✅ 最终版Qji Max引擎初始化完成！")
    
    def generate_response(self, message: str, conversation_history=None):
        """
        Generate response with smart routing based on query type
        """
        if self.smart_router.should_handle_date_query(message):
            # Handle date queries with pre-verified accurate data
            return self.smart_router.handle_date_query(message, conversation_history)
        else:
            # Handle general queries with Qwen Max Thinking mode
            return self.smart_router.handle_general_query(message, conversation_history)
    
    def analyze_bazi(self, birth_date: str, birth_time: str, gender: str, location: str) -> str:
        """
        Analyze bazi with enhanced capabilities
        """
        prompt = f"""
请为我详细分析这个八字：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

需要包含以下内容：
1. 四柱八字排盘（年柱、月柱、日柱、时柱）
2. 日主强弱分析
3. 格局判断和用神选择
4. 大运流年分析
5. 具体的人生建议（事业、财运、感情、健康）

请基于十大命理经典的理论进行专业分析。
"""
        
        return self.smart_router.handle_general_query(prompt, [])