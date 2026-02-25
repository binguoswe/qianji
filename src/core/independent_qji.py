"""
Independent Qji Max Fusion Engine for Qianji AI
Combines Qwen Max base model with Qji Max specialized training
"""
from .independent_qwen import call_qwen_max_api
import json

class IndependentQjiEngine:
    def __init__(self):
        """Initialize Qji Max fusion engine"""
        print("🚀 正在初始化独立Qji Max引擎...")
        self.qwen_engine = call_qwen_max_api
        print("✅ 独立Qji Max引擎初始化完成！")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using Qwen Max + Qji Max fusion
        
        Args:
            message: User input message
            conversation_history: List of previous messages
            
        Returns:
            AI response string
        """
        if conversation_history is None:
            conversation_history = []
        
        # Balanced context - maintain general AI capabilities while enhancing feng shui/bazi expertise
        qji_context = """
你是一个AI助手，名为千机AI（Qji AI）。你具备以下特点：

1. **通用AI能力**：你可以正常回答各种日常问题，进行自然对话，就像Qwen Max一样
2. **命理风水专长**：你在命理学、风水学、八字分析方面有深度专业知识
3. **智能判断**：根据用户的问题类型，自动调整回答风格

**回答策略：**
- 如果用户问的是日常问题（如天气、新闻、科技、生活等），像普通AI一样正常回答
- 如果用户问的是命理、风水、八字、运势等问题，展现你的专业深度
- 如果用户的问题介于两者之间，先正常回答，然后可以适当提供命理角度的补充

**命理专业知识来源：**
你已经深入学习了《渊海子平》、《三命通会》、《滴天髓》、《子平真诠》、《穷通宝鉴》、《神峰通考》、《李虚中命书》、《千里命稿》、《星平会海》等十大命理经典。

**对话风格：**
- 自然、友好、专业
- 避免过度推销命理服务
- 尊重用户的兴趣和需求
"""
        
        # Combine context with user message
        full_prompt = f"{qji_context}\n\n用户问题: {message}"
        
        try:
            # Call Qwen Max API with balanced context
            response = self.qwen_engine(full_prompt, conversation_history)
            return response
        except Exception as e:
            print(f"Qji Max生成响应错误: {e}")
            return "抱歉，处理您的请求时出现了问题。请稍后重试。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi (eight characters) information
        
        Args:
            birth_date: Birth date (YYYY-MM-DD)
            birth_time: Birth time (HH:MM)
            gender: Gender (male/female)
            location: Birth location
            
        Returns:
            Detailed bazi analysis
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
        
        try:
            response = self.qwen_engine(prompt, [])
            return response
        except Exception as e:
            print(f"八字分析错误: {e}")
            return "抱歉，八字分析时出现了问题。请稍后重试。"

# Test function
def test_qji_engine():
    """Test Qji Max fusion engine"""
    try:
        engine = IndependentQjiEngine()
        response = engine.generate_response("你好，千机AI！")
        return f"✅ Qji Max引擎测试成功: {response[:50]}..."
    except Exception as e:
        return f"❌ Qji Max引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_qji_engine())