"""
Independent Qji Fixed Bazi Engine for Qianji AI - Uses Authoritative Bazi Tools
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

# Import Qwen Max API
from src.core.independent_qwen import call_qwen_max_api

# Import authoritative bazi validator
try:
    from src.core.authoritative_bazi_validator import AuthoritativeBaziValidator
    bazi_validator_available = True
    bazi_validator = AuthoritativeBaziValidator()
except ImportError:
    print("警告: 未找到权威八字验证器，将使用基础模式")
    bazi_validator_available = False
    bazi_validator = None

class IndependentQjiFixedBaziEngine:
    def __init__(self):
        """Initialize Qji Fixed Bazi engine with authoritative tools"""
        print("🚀 正在初始化千机AI引擎（八字修正版）...")
        self.use_lunar = LunarDate is not None and Lunar is not None
        if self.use_lunar:
            print("✅ 农历功能已启用")
        else:
            print("⚠️  农历功能不可用，使用基础日期")
            
        if bazi_validator_available:
            print("✅ 权威八字验证器已启用")
        else:
            print("⚠️  权威八字验证器不可用")
            
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
            "hour": now.hour,
            "minute": now.minute,
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
                 "七月", "八月", "九月", "十月", "冬日消息", "腊月"]
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
    
    def validate_and_get_bazi(self, birth_date, birth_time):
        """Use authoritative tools to get accurate bazi"""
        if bazi_validator_available:
            # Try to get validated bazi data
            validated_data = bazi_validator.validate_bazi(birth_date, birth_time)
            if validated_data:
                return validated_data
        
        # If no validated data available, return None to indicate need for manual calculation
        return None
    
    def generate_response(self, message, conversation_history=None):
        """
        Generate response using Qwen Max API with real-time date context
        """
        if conversation_history is None:
            conversation_history = []
        
        # Get current date info
        date_info = self.get_current_date_info()
        
        # Build context with real date information
        if date_info["lunar_info"]:
            date_context = f"当前公历日期是{date_info['solar_date']}（{date_info['weekday']}），农历日期是{date_info['lunar_info']}。"
        else:
            date_context = f"当前日期是{date_info['solar_date']}（{date_info['weekday']}）。"
        
        qji_context = f"""
你是一个AI助手，名为千机AI（Qji AI）。

{date_context}

你具备以下特点：

1. **通用AI能力**：你可以正常回答各种日常问题，进行自然对话，就像Qwen Max一样
2. **命理风水专长**：你在命理学、风水学、八字分析方面有深度专业知识
3. **智能判断**：根据用户的问题类型，自动调整回答风格

**重要提示：**
- 当前年份是{date_info['year']}年
- 当前时间是{date_info['hour']}点{date_info['minute']}分
- 请确保所有日期相关的回答都基于上述真实日期信息
- 如果提供了真实农历日期，请优先使用该信息进行命理分析

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
        
        # Combine context with user message
        full_prompt = f"{qji_context}\n\n用户问题: {message}"
        
        try:
            # Call Qwen Max API with thinking mode enabled
            response = call_qwen_max_api(full_prompt, conversation_history)
            return response
        except Exception as e:
            print(f"Qji Fixed Bazi生成响应错误: {e}")
            return "抱歉，处理您的请求时出现了问题。请稍后重试。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi using authoritative tools first, then Qwen Max for analysis
        """
        # First, try to get authoritative bazi data
        authoritative_bazi = self.validate_and_get_bazi(birth_date, birth_time)
        
        if authoritative_bazi:
            # Use authoritative data to generate prompt
            current_date_info = self.get_current_date_info()
            current_context = f"当前公历日期：{current_date_info['solar_date']}（{current_date_info['weekday']}）"
            if current_date_info.get('lunar_info'):
                current_context += f"\n当前农历日期：{current_date_info['lunar_info']}"
            
            prompt = f"""
{current_context}

我已经通过权威万年历验证了您的八字信息：

**基本信息**：
- 公历出生：{birth_date} {birth_time}
- 农历出生：{authoritative_bazi['lunar_date']}
- 性别：{gender}
- 出生地：{location}

**八字排盘（经权威验证）**：
- 年柱：{authoritative_bazi['year_pillar']}
- 月柱：{authoritative_bazi['month_pillar']}  
- 日柱：{authoritative_bazi['day_pillar']}
- 时柱：{authoritative_bazi.get('hour_pillar', '需根据具体时间确定')}
- 完整八字：{authoritative_bazi.get('full_bazi', '待确认')}

请基于以上准确的八字信息，结合十大命理经典的理论，为我提供详细的专业分析：

1. **日主强弱分析**：分析日主在八字中的旺衰状态
2. **格局判断**：确定具体的命格类型（正官格、七杀格、财格等）
3. **用神选择**：根据格局和日主强弱确定用神
4. **大运流年**：分析当前大运和近期流年走势
5. **人生建议**：提供事业、财运、感情、健康等方面的具体建议

请确保分析的专业性和准确性。
"""
        else:
            # Fallback to standard prompt if no authoritative data
            date_info = self.get_current_date_info()
            current_date_info = f"当前公历日期：{date_info['solar_date']}（{date_info['weekday']}）"
            if date_info.get('lunar_info'):
                current_date_info += f"\n当前农历日期：{date_info['lunar_info']}"
            
            prompt = f"""
{current_date_info}

请为我详细分析这个八字：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

需要包含以下内容：
1. 四柱八字排盘（年柱、月柱、日柱、时柱）
2. 日主强弱分析
3. 格局判断和用神选择
4. 大运流年分析（基于当前年份{date_info['year']}）
5. 具体的人生建议（事业、财运、感情、健康）

请基于十大命理经典的理论进行专业分析，并确保八字排盘的准确性。
"""
        
        try:
            response = call_qwen_max_api(prompt, [])
            return response
        except Exception as e:
            print(f"八字分析错误: {e}")
            return "抱歉，八字分析时出现了问题。请稍后重试。"

# Test function
def test_qji_fixed_bazi_engine():
    """Test Qji Fixed Bazi engine"""
    try:
        engine = IndependentQjiFixedBaziEngine()
        date_info = engine.get_current_date_info()
        print(f"✅ 日期信息获取成功: {date_info}")
        
        # Test bazi validation
        if bazi_validator_available:
            test_bazi = engine.validate_and_get_bazi("2026-02-25", "23:00")
            print(f"✅ 八字验证测试: {test_bazi is not None}")
        
        response = engine.generate_response("你好，千机AI！")
        print(f"✅ 响应生成成功: {response[:50]}...")
        
        return "✅ Qji Fixed Bazi引擎测试成功"
    except Exception as e:
        return f"❌ Qji Fixed Bazi引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_qji_fixed_bazi_engine())