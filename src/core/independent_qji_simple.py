"""
Independent Qji Simple Engine for Qianji AI - Real-time Date Handling
Simple version that uses system time instead of web search for date context
"""
from datetime import datetime
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

try:
    from lunardate import LunarDate
    from cnlunar import Lunar
except ImportError:
    print("警告: 未安装农历库，将使用基础日期功能")
    LunarDate = None
    Lunar = None

class IndependentQjiEngine:
    def __init__(self):
        """Initialize Qji Simple engine with real-time date handling"""
        print("🚀 正在初始化千机AI引擎（简化版）...")
        self.use_lunar = LunarDate is not None and Lunar is not None
        if self.use_lunar:
            print("✅ 农历功能已启用")
        else:
            print("⚠️  农历功能不可用，使用基础日期")
        print("✅ 千机AI引擎初始化完成！")
    
    def get_current_date_info(self):
        """Get current date information with lunar conversion if available"""
        now = datetime.now()
        solar_date = now.strftime("%Y-%m-%d")
        weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekday_names[now.weekday()]
        
        result = {
            "solar_date": solar_date,
            "weekday": weekday,
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "lunar_info": None
        }
        
        # Try to get lunar date if libraries are available
        if self.use_lunar:
            try:
                lunar_date = LunarDate.fromSolarDate(now.year, now.month, now.day)
                lunar_str = f"{lunar_date.year}年{self._get_lunar_month_name(lunar_date.month)}{self._get_lunar_day_name(lunar_date.day)}"
                if hasattr(lunar_date, 'isLeapMonth') and lunar_date.isLeapMonth:
                    lunar_str = f"{lunar_date.year}年闰{self._get_lunar_month_name(lunar_date.month)}{self._get_lunar_day_name(lunar_date.day)}"
                
                result["lunar_info"] = lunar_str
            except Exception as e:
                print(f"农历转换错误: {e}")
                result["lunar_info"] = None
        
        return result
    
    def _get_lunar_month_name(self, month):
        """Get lunar month name"""
        months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                 "七月", "八月", "九月", "十月", "冬月", "腊月"]
        return months[month - 1] if 1 <= month <= 12 else f"{month}月"
    
    def _get_lunar_day_name(self, day):
        """Get lunar day name"""
        if day <= 10:
            days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十"]
            return days[day - 1]
        elif day <= 20:
            return f"十{['一', '二', '三', '四', '五', '六', '七', '八', '九', ''][day - 11]}"
        elif day <= 30:
            if day == 20:
                return "二十"
            elif day < 30:
                return f"廿{['一', '二', '三', '四', '五', '六', '七', '八', '九', ''][day - 21]}"
            else:
                return "三十"
        return f"{day}日"
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using real-time date context
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get current date info
        date_info = self.get_current_date_info()
        
        # Build context
        if date_info["lunar_info"]:
            date_context = f"当前公历日期是{date_info['solar_date']}（{date_info['weekday']}），农历日期是{date_info['lunar_info']}。"
        else:
            date_context = f"当前日期是{date_info['solar_date']}（{date_info['weekday']}）。"
        
        qji_context = f"""
你是一个AI助手，名为千机AI（Qji AI）。

{date_context}

你具备以下特点：

1. **通用AI能力**：你可以正常回答各种日常问题，进行自然对话
2. **命理风水专长**：你在命理学、风水学、八字分析方面有深度专业知识
3. **智能判断**：根据用户的问题类型，自动调整回答风格

**重要提示：**
- 当前年份是{date_info['year']}年
- 请确保所有日期相关的回答都基于上述真实日期信息

**命理专业知识来源：**
你已经深入学习了《渊海子平》、《三命通会》、《滴天髓》、《子平真诠》、《穷通宝鉴》、《神峰通考》、《李虚中命书》、《千里命稿》、《星平会海》等十大命理经典。

**回答策略：**
- 如果用户问的是日常问题（如天气、新闻、科技、生活等），像普通AI一样正常回答
- 如果用户问的是命理、风水、八字、运势等问题，展现你的专业深度
- 如果用户的问题涉及日期，请务必使用上述真实日期信息

**对话风格：**
- 自然、友好、专业
- 避免过度推销命理服务
- 尊重用户的兴趣和需求
"""
        
        # For now, return a simple response since we don't have the Qwen API integrated
        # In a real implementation, this would call the actual AI model
        if "今天" in message or "日期" in message or "农历" in message:
            if date_info["lunar_info"]:
                return f"今天是{date_info['solar_date']}（{date_info['weekday']}），农历{date_info['lunar_info']}。"
            else:
                return f"今天是{date_info['solar_date']}（{date_info['weekday']}）。"
        elif "你好" in message or "hello" in message.lower():
            return "你好！我是千机AI，可以为你提供命理、风水、八字分析等专业咨询服务，也可以回答日常问题。有什么我可以帮你的吗？"
        else:
            return "我收到了你的消息。如果你有关于命理、风水、八字的问题，或者需要日常帮助，请告诉我具体需求。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi (eight characters) information
        """
        date_info = self.get_current_date_info()
        
        current_date_info = f"当前公历日期：{date_info['solar_date']}（{date_info['weekday']}）"
        if date_info.get('lunar_info'):
            current_date_info += f"\n当前农历日期：{date_info['lunar_info']}"
        
        return f"""
【八字分析请求已接收】

基本信息：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

当前日期参考：
{current_date_info}

由于千机AI的完整八字分析功能需要调用专业AI模型，目前简化版返回基本信息确认。
在完整版本中，我会提供详细的四柱排盘、日主强弱分析、格局判断、大运流年分析等专业内容。

请确认以上信息是否正确，或提供更多具体问题。
"""

# Test function
def test_qji_engine():
    """Test Qji Simple engine"""
    try:
        engine = IndependentQjiEngine()
        date_info = engine.get_current_date_info()
        print(f"✅ 日期信息获取成功: {date_info}")
        
        response = engine.generate_response("今天是什么日子？")
        print(f"✅ 响应生成成功: {response}")
        
        return "✅ Qji Simple引擎测试成功"
    except Exception as e:
        return f"❌ Qji Simple引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_qji_engine())