"""
Independent Qji Max Fusion Engine for Qianji AI - Smart Search Enabled
Combines Qwen Max base model with Qji Max specialized training and native web search
"""
from .qwen_max_with_search import call_qwen_max_with_search
import json
from datetime import datetime

class IndependentQjiEngine:
    def __init__(self):
        """Initialize Qji Max fusion engine with smart search"""
        print("🚀 正在初始化独立Qji Max引擎（智能搜索版）...")
        self.qwen_engine = call_qwen_max_with_search
        print("✅ 独立Qji Max引擎（智能搜索版）初始化完成！")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using Qwen Max + Qji Max fusion with native web search
        
        Args:
            message: User input message
            conversation_history: List of previous messages
            
        Returns:
            AI response string
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get current date context
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        # Enhanced context that encourages smart behavior
        qji_context = f"""
你是一个AI助手，名为千机AI（Qji AI）。当前日期是{current_date}，{current_weekday}。

你具备以下特点：

1. **通用AI能力**：你可以正常回答各种日常问题，进行自然对话，就像Qwen Max一样
2. **命理风水专长**：你在命理学、风水学、八字分析方面有深度专业知识  
3. **智能验证能力**：对于关键事实信息（如日期、数字、历史事件等），你会自动联网搜索验证
4. **自我校验**：你会交叉验证信息确保准确性，避免提供错误答案

**重要行为准则：**
- 当涉及日期、农历、黄历等时间相关信息时，必须联网搜索验证
- 当涉及具体数字、事实、统计数据时，必须联网搜索验证  
- 当不确定某个信息的准确性时，主动联网搜索
- 优先使用权威来源（官方万年历、政府网站、知名媒体等）
- 如果搜索结果不一致，明确告知用户并说明差异

**命理专业知识来源：**
你已经深入学习了《渊海子平》、《三命通会》、《滴天髓》、《子平真诠》、《穷通宝鉴》、《神峰通考》、《李虚中命书》、《千里命稿》、《星平会海》等十大命理经典。

**对话风格：**
- 自然、友好、专业
- 避免过度推销命理服务
- 尊重用户的兴趣和需求
- 对于不确定的信息，诚实说明并主动验证
"""
        
        # Combine context with user message
        full_prompt = f"{qji_context}\n\n用户问题: {message}"
        
        try:
            # Call Qwen Max API with native web search enabled
            response = self.qwen_engine(full_prompt, conversation_history)
            return response
        except Exception as e:
            print(f"Qji Max生成响应错误: {e}")
            return "抱歉，处理您的请求时出现了问题。请稍后重试。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi (eight characters) information with smart search
        """
        # Get current date context
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        prompt = f"""
当前日期：{current_date}，{current_weekday}

请为我详细分析这个八字：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

需要包含以下内容：
1. 四柱八字排盘（年柱、月柱、日柱、时柱）
2. 日主强弱分析
3. 格局判断和用神选择
4. 大运流年分析（基于当前年份{now.year}）
5. 具体的人生建议（事业、财运、感情、健康）

**重要要求：**
- 所有日期计算必须准确无误
- 如有不确定的地方，请联网搜索验证
- 基于十大命理经典的理论进行专业分析
"""
        
        try:
            response = self.qwen_engine(prompt, [])
            return response
        except Exception as e:
            print(f"八字分析错误: {e}")
            return "抱歉，八字分析时出现了问题。请稍后重试。"

# Test function
def test_qji_engine():
    """Test Qji Max fusion engine with smart search"""
    try:
        engine = IndependentQjiEngine()
        response = engine.generate_response("今天农历是多少？")
        return f"✅ Qji Max智能搜索引擎测试成功: {response[:100]}..."
    except Exception as e:
        return f"❌ Qji Max智能搜索引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_qji_engine())