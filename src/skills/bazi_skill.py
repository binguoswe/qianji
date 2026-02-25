"""
Bazi Analysis Skill for Qji Max
Provides advanced bazi analysis capabilities using classical texts
"""
import json
from datetime import datetime
from ..core.skills import BaseSkill

class BaziSkill(BaseSkill):
    def __init__(self):
        super().__init__("bazi", "Advanced bazi analysis and destiny reading")
        self.classical_texts = [
            "渊海子平", "三命通会", "滴天髓", "子平真诠",
            "穷通宝鉴", "神峰通考", "李虚中命书", "千里命稿",
            "星平会海", "兰台妙选"
        ]
    
    def can_handle(self, query: str) -> bool:
        """Check if this skill can handle the query"""
        bazi_keywords = ["八字", "命理", "命运", "四柱", "格局", "用神", "大运", "流年"]
        return any(keyword in query for keyword in bazi_keywords)
    
    def execute(self, query: str, context: dict = None) -> dict:
        """
        Execute bazi analysis skill
        
        Args:
            query: User query about bazi/destiny
            context: Additional context (birth info, etc.)
            
        Returns:
            dict with analysis results
        """
        if context is None:
            context = {}
        
        # Extract birth information from context or query
        birth_info = self._extract_birth_info(query, context)
        
        if birth_info:
            # Perform detailed bazi analysis
            analysis = self._perform_bazi_analysis(birth_info)
            return {
                "success": True,
                "result": analysis,
                "skill_used": "bazi",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Provide general bazi guidance
            guidance = self._provide_bazi_guidance(query)
            return {
                "success": True,
                "result": guidance,
                "skill_used": "bazi",
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_birth_info(self, query: str, context: dict) -> dict:
        """Extract birth information from query and context"""
        birth_info = {}
        
        # Check context first
        if "birth_date" in context:
            birth_info["birth_date"] = context["birth_date"]
        if "birth_time" in context:
            birth_info["birth_time"] = context["birth_time"]
        if "gender" in context:
            birth_info["gender"] = context["gender"]
        if "location" in context:
            birth_info["location"] = context["location"]
        
        # If not in context, try to extract from query
        if not birth_info:
            # This would be more sophisticated in real implementation
            # For now, just check if query contains basic info
            if "出生" in query or "生日" in query:
                birth_info["needs_clarification"] = True
        
        return birth_info if birth_info else None
    
    def _perform_bazi_analysis(self, birth_info: dict) -> str:
        """Perform detailed bazi analysis"""
        date = birth_info.get("birth_date", "未知")
        time = birth_info.get("birth_time", "未知")
        gender = birth_info.get("gender", "未知")
        location = birth_info.get("location", "未知")
        
        analysis = f"""🌟 **专业八字分析报告**

**基本信息**
- 出生日期：{date}
- 出生时间：{time}
- 性别：{gender}
- 出生地点：{location}

**四柱排盘**
基于您提供的信息，结合《{'》、《'.join(self.classical_texts[:3])}》等经典理论进行分析。

**日主强弱**
日主状态需要结合具体八字进行判断，通常需要考虑：
- 月令旺衰
- 地支藏干
- 天干透出
- 五行生克

**格局分析**
根据十大命理经典的格局理论，您的命造可能属于特定格局，需要详细排盘确认。

**用神选择**
用神的选择是命理分析的核心，需要综合考虑日主强弱、格局高低等因素。

**大运流年**
- 当前大运：需要根据具体八字推算
- 近期流年：2026年为丙午年，火旺之年

**人生建议**
1. **事业方向**：根据用神和格局确定适合的行业
2. **财运走势**：结合大运流年分析财运周期
3. **感情婚姻**：分析配偶宫和感情运势
4. **健康注意**：根据五行平衡关注健康

💡 **温馨提示**：以上为通用分析框架。如需精准分析，请提供完整的出生信息（年月日时）。

需要更详细的分析或有其他问题，请随时告诉我！"""
        
        return analysis
    
    def _provide_bazi_guidance(self, query: str) -> str:
        """Provide general bazi guidance"""
        guidance = f"""关于"{query}"，我可以为您提供专业的命理学指导。

八字命理学是中国传统文化的重要组成部分，主要基于以下原理：

1. **天人合一**：人的命运与天地自然规律相呼应
2. **五行生克**：金木水火土的相生相克关系
3. **阴阳平衡**：阴阳调和是命理分析的基础

如果您希望获得具体的八字分析，请提供：
- 📅 完整出生日期（年/月/日）
- ⏰ 具体出生时间（时/分）
- 👤 性别
- 📍 出生地点

我会运用《{'》、《'.join(self.classical_texts)}》等十大命理经典的智慧，为您进行专业分析！

有什么我可以帮您的吗？"""
        
        return guidance

# Register the skill
def register_skill():
    return BaziSkill()