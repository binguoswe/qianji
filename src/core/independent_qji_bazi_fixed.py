"""
Fixed Qji Max Engine with Authoritative Bazi Validation
Ensures accurate bazi calculations using verified authoritative sources
"""
from .authoritative_bazi_validator import AuthoritativeBaziValidator

class IndependentQjiBaziFixedEngine:
    def __init__(self):
        """Initialize fixed Qji Max engine with authoritative bazi validation"""
        print("🚀 正在初始化修复版Qji Max引擎（权威八字验证）...")
        self.bazi_validator = AuthoritativeBaziValidator()
        print("✅ 修复版Qji Max引擎初始化完成！")
    
    def generate_response(self, message: str, conversation_history=None):
        """
        Generate response with proper identity and capabilities
        """
        # For now, use the identity-fixed version
        from .independent_qji_identity import IndependentQjiIdentityEngine
        identity_engine = IndependentQjiIdentityEngine()
        return identity_engine.generate_response(message, conversation_history)
    
    def analyze_bazi(self, birth_date: str, birth_time: str, gender: str, location: str) -> str:
        """
        Analyze bazi with authoritative validation
        """
        # Try to get authoritative response first
        authoritative_response = self.bazi_validator.get_authoritative_response(
            birth_date, birth_time, gender, location
        )
        
        if authoritative_response:
            return authoritative_response
        
        # Fall back to model-based analysis if no authoritative data
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
        
        from .independent_qji_identity import IndependentQjiIdentityEngine
        identity_engine = IndependentQjiIdentityEngine()
        return identity_engine.generate_response(prompt, [])