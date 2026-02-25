"""
Final Qji Max Engine with Identity Fix and Smart Routing
Ensures Qwen Max always identifies as Qji, not Qwen
"""
from .smart_router_identity import SmartRouterIdentity

class IndependentQjiIdentityEngine:
    def __init__(self):
        """Initialize final Qji Max engine with identity fix"""
        print("🚀 正在初始化千机AI引擎（身份修复版）...")
        self.smart_router = SmartRouterIdentity()
        print("✅ 千机AI引擎（身份修复版）初始化完成！")
    
    def generate_response(self, message: str, conversation_history=None):
        """
        Generate response with smart routing and proper identity
        """
        if self.smart_router.should_handle_date_query(message):
            # Handle date queries with pre-verified accurate data
            return self.smart_router.handle_date_query(message, conversation_history)
        else:
            # Handle general queries with Qwen Max Thinking mode and proper identity
            return self.smart_router.handle_general_query(message, conversation_history)
    
    def analyze_bazi(self, birth_date: str, birth_time: str, gender: str, location: str) -> str:
        """
        Analyze bazi with enhanced capabilities and proper identity
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