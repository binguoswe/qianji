"""
Independent Qji Max Smart Engine with Native Web Search and Verification
Uses Qwen Max's built-in search capability with smart verification
"""
from .qwen_max_with_search import call_qwen_max_with_search
from .smart_verification import add_verification_note
import json
from datetime import datetime

class IndependentQjiSmartEngine:
    def __init__(self):
        """Initialize Qji Max smart engine with native search"""
        print("🚀 正在初始化独立Qji Max智能引擎（原生联网搜索版）...")
        self.qwen_engine = call_qwen_max_with_search
        print("✅ 独立Qji Max智能引擎（原生联网搜索版）初始化完成！")
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using Qwen Max with native search and verification
        
        Args:
            message: User input message
            conversation_history: List of previous messages
            
        Returns:
            AI response string with verification notes if needed
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get current date context for reference
        now = datetime.now()
        current_date = now.strftime("%Y年%m月%d日")
        current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
        
        # Enhanced context with verification instructions
        qji_context = f"""
你是一个AI助手，名为千机AI（Qji AI）。当前日期是{current_date}，{current_weekday}。

你的特点：
1. **通用AI能力**：正常回答各种日常问题
2. **命理风水专长**：深度专业知识  
3. **联网搜索能力**：已启用原生联网搜索功能
4. **智能验证**：对关键信息（日期、数字、事实）进行交叉验证

**重要指令：**
- 当回答涉及日期、农历、黄历等关键信息时，必须使用联网搜索获取最新准确数据
- 如果对某个信息不确定，请明确说明并建议用户通过权威渠道验证
- 保持诚实和透明，不要猜测不确定的信息
- 优先使用权威万年历网站的数据（如中国万年历、老黄历等）

**命理专业知识来源：**
《渊海子平》、《三命通会》、《滴天髓》、《子平真诠》、《穷通宝鉴》、《神峰通考》、《李虚中命书》、《千里命稿》、《星平会海》等十大命理经典。
"""
        
        full_prompt = f"{qji_context}\n\n用户问题: {message}"
        
        try:
            # Call Qwen Max with native search enabled
            response = self.qwen_engine(full_prompt, conversation_history)
            
            # Add verification note for date-related responses
            if any(keyword in message for keyword in ['今天', '日期', '农历', '阴历', '阳历', '公历', '正月', '腊月']):
                response = add_verification_note(response)
            
            return response
        except Exception as e:
            print(f"Qji Max生成响应错误: {e}")
            return "抱歉，处理您的请求时出现了问题。请稍后重试。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi with enhanced capabilities
        """
        prompt = f"""
当前日期：{datetime.now().strftime("%Y年%m月%d日")}

请为我详细分析这个八字：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

需要包含以下内容：
1. 四柱八字排盘（年柱、月柱、日柱、时柱）
2. 日主强弱分析
3. 格局判断和用神选择
4. 大运流年分析（基于当前年份）
5. 具体的人生建议（事业、财运、感情、健康）

请基于十大命理经典的理论进行专业分析，并确保所有日期计算准确无误。
"""
        
        try:
            response = self.qwen_engine(prompt, [])
            return response
        except Exception as e:
            print(f"八字分析错误: {e}")
            return "抱歉，八字分析时出现了问题。请稍后重试。"

# Test function
def test_qji_smart_engine():
    """Test Qji Max smart engine"""
    try:
        engine = IndependentQjiSmartEngine()
        response = engine.generate_response("今天农历是多少？")
        return f"✅ Qji Max智能引擎测试成功:\n{response[:100]}..."
    except Exception as e:
        return f"❌ Qji Max智能引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_qji_smart_engine())