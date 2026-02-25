"""
Pure Qwen Max Thinking Mode Engine for Qianji AI
Completely relies on Qwen Max's native thinking and decision capabilities
No external rules or interventions - let the model decide everything autonomously
"""
from .qwen_max_pure_thinking import call_qwen_max_pure_thinking

class IndependentQjiPureThinkingEngine:
    def __init__(self):
        """Initialize pure thinking engine"""
        print("🚀 正在初始化纯Thinking模式Qji Max引擎...")
        print("✅ 完全依赖Qwen Max自主决策，无任何人工干预")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using pure Qwen Max thinking mode
        Let the model completely decide when to search and how to respond
        """
        return call_qwen_max_pure_thinking(message, conversation_history)
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi using pure thinking mode
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
        return call_qwen_max_pure_thinking(prompt, [])