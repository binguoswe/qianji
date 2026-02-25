"""
Independent Qji Max Engine with Qwen Max Thinking Mode
Uses native web search and thinking capabilities
"""
from .qwen_max_thinking import call_qwen_max_thinking
import json
from datetime import datetime

class IndependentQjiThinkingEngine:
    def __init__(self):
        """Initialize Qji Max engine with thinking mode"""
        print("🚀 正在初始化独立Qji Max引擎（Thinking模式）...")
        self.qwen_engine = call_qwen_max_thinking
        print("✅ 独立Qji Max引擎（Thinking模式）初始化完成！")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using Qwen Max Thinking mode with native search
        """
        if conversation_history is None:
            conversation_history = []
        
        # Enhanced context for thinking mode
        current_date = datetime.now().strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][datetime.now().weekday()]
        
        thinking_context = f"""
你是一个专业的命理AI助手，名为千机AI（Qji AI）。当前日期是{current_date}，{current_weekday}。

你正在使用Qwen Max的Thinking模式，具备以下能力：
1. **深度思考**：对复杂问题进行多步推理
2. **联网搜索**：自动获取最新、最准确的信息
3. **自我验证**：交叉验证信息确保准确性
4. **专业分析**：基于十大命理经典提供专业见解

**重要提示**：
- 当涉及日期、农历、黄历等关键信息时，必须通过联网搜索验证
- 提供的答案必须准确无误，如有不确定请明确说明
- 保持专业、友好、诚实的态度

用户问题: {message}
"""
        
        try:
            response = self.qwen_engine(thinking_context, conversation_history)
            return response
        except Exception as e:
            print(f"Thinking engine error: {e}")
            return "抱歉，处理您的请求时出现了问题。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi with thinking mode
        """
        prompt = f"""
请为我详细分析这个八字：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

使用Thinking模式进行深度分析，确保所有信息准确无误。
"""
        
        try:
            response = self.qwen_engine(prompt, [])
            return response
        except Exception as e:
            print(f"Bazi analysis error: {e}")
            return "抱歉，八字分析时出现了问题。"

# Test function
def test_thinking_engine():
    """Test thinking engine"""
    try:
        engine = IndependentQjiThinkingEngine()
        response = engine.generate_response("今天农历是多少？")
        return f"✅ Thinking引擎测试成功: {response[:100]}..."
    except Exception as e:
        return f"❌ Thinking引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_thinking_engine())