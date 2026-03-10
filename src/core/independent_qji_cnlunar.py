"""
Independent Qji Engine with CNLunar Integration for Accurate Bazi Calculation
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
    cnlunar_available = True
except ImportError:
    print("警告: 未安装农历库，将使用基础日期功能")
    LunarDate = None
    Lunar = None
    cnlunar_available = False

# Import Qwen Max API
from src.core.independent_qwen import call_qwen_max_api

class IndependentQjiCnlunarEngine:
    def __init__(self):
        """Initialize Qji engine with CNLunar integration"""
        print("🚀 正在初始化千机AI引擎（CNLunar集成版）...")
        self.use_lunar = LunarDate is not None and Lunar is not None
        if self.use_lunar:
            print("✅ 农历功能已启用")
        else:
            print("⚠️  农历功能不可用，使用基础日期")
            
        if cnlunar_available:
            print("✅ CNLunar八字计算库已启用")
        else:
            print("⚠️  CNLunar八字计算库不可用")
            
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
            "lunar_info": None,
            "bazi_info": None
        }
        
        # Try to get lunar date and bazi if libraries are available
        if cnlunar_available:
            try:
                lunar_obj = Lunar(now)
                lunar_str = f"{lunar_obj.lunarYear}年{self._get_lunar_month_name(lunar_obj.lunarMonth)}{self._get_lunar_day_name(lunar_obj.lunarDay)}"
                
                # Get accurate bazi information
                bazi_info = {
                    "year_pillar": lunar_obj.year8Char,
                    "month_pillar": lunar_obj.month8Char,
                    "day_pillar": lunar_obj.day8Char,
                    "hour_pillar": self._get_hour_pillar(now.hour, lunar_obj.day8Char[0]),
                    "full_bazi": f"{lunar_obj.year8Char} {lunar_obj.month8Char} {lunar_obj.day8Char} {self._get_hour_pillar(now.hour, lunar_obj.day8Char[0])}"
                }
                
                result["lunar_info"] = lunar_str
                result["bazi_info"] = bazi_info
                
            except Exception as e:
                print(f"农历和八字转换错误: {e}")
                result["lunar_info"] = None
                result["bazi_info"] = None
        
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
    
    def _get_hour_pillar(self, hour, day_gan):
        """Get hour pillar based on day heavenly stem and hour"""
        # 天干：甲、乙、丙、丁、戊、己、庚、辛、壬、癸
        # 地支：子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥
        
        # 五鼠遁口诀
        gan_index = {"甲": 0, "乙": 0, "丙": 2, "丁": 2, "戊": 4, "己": 4, "庚": 6, "辛": 6, "壬": 8, "癸": 8}
        base_gan_index = gan_index.get(day_gan, 0)
        
        # 时辰地支索引 (子=0, 丑=1, ..., 亥=11)
        if hour == 23 or hour == 0:
            time_index = 0  # 子时
        elif 1 <= hour <= 2:
            time_index = 1  # 丑时
        elif 3 <= hour <= 4:
            time_index = 2  # 寅时
        elif 5 <= hour <= 6:
            time_index = 3  # 卯时
        elif 7 <= hour <= 8:
            time_index = 4  # 辰时
        elif 9 <= hour <= 10:
            time_index = 5  # 巳时
        elif 11 <= hour <= 12:
            time_index = 6  # 午时
        elif 13 <= hour <= 14:
            time_index = 7  # 未时
        elif 15 <= hour <= 16:
            time_index = 8  # 申时
        elif 17 <= hour <= 18:
            time_index = 9  # 酉时
        elif 19 <= hour <= 20:
            time_index = 10  # 戌时
        elif 21 <= hour <= 22:
            time_index = 11  # 亥时
        else:
            time_index = 0  # 默认子时
        
        # 计算时柱天干
        hour_gan_index = (base_gan_index + time_index) % 10
        heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        return f"{heavenly_stems[hour_gan_index]}{earthly_branches[time_index]}"
    
    def get_accurate_bazi(self, birth_datetime):
        """Get accurate bazi using CNLunar library"""
        if not cnlunar_available:
            return None
        
        try:
            lunar_obj = Lunar(birth_datetime)
            hour = birth_datetime.hour
            day_gan = lunar_obj.day8Char[0]
            hour_pillar = self._get_hour_pillar(hour, day_gan)
            
            bazi_info = {
                "year_pillar": lunar_obj.year8Char,
                "month_pillar": lunar_obj.month8Char,
                "day_pillar": lunar_obj.day8Char,
                "hour_pillar": hour_pillar,
                "full_bazi": f"{lunar_obj.year8Char} {lunar_obj.month8Char} {lunar_obj.day8Char} {hour_pillar}",
                "lunar_year": lunar_obj.lunarYear,
                "lunar_month": lunar_obj.lunarMonth,
                "lunar_day": lunar_obj.lunarDay,
                "is_leap_month": lunar_obj.isLunarLeapMonth
            }
            
            return bazi_info
            
        except Exception as e:
            print(f"八字计算错误: {e}")
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
            if date_info["bazi_info"]:
                date_context += f"\n当前八字是：{date_info['bazi_info']['full_bazi']}。"
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
            print(f"Qji CNLunar生成响应错误: {e}")
            return "抱歉，处理您的请求时出现了问题。请稍后重试。"
    
    def analyze_bazi(self, birth_date, birth_time, gender, location):
        """
        Analyze bazi using CNLunar for accurate calculation, then Qwen Max for analysis
        """
        # Parse birth datetime
        from datetime import datetime
        try:
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return "出生日期或时间格式错误，请使用 YYYY-MM-DD 和 HH:MM 格式。"
        
        # Get accurate bazi using CNLunar
        accurate_bazi = self.get_accurate_bazi(birth_datetime)
        
        if accurate_bazi:
            # Use accurate bazi data to generate prompt
            current_date_info = self.get_current_date_info()
            current_context = f"当前公历日期：{current_date_info['solar_date']}（{current_date_info['weekday']}）"
            if current_date_info.get('lunar_info'):
                current_context += f"\n当前农历日期：{current_date_info['lunar_info']}"
            
            # Determine lunar month name
            lunar_month_name = self._get_lunar_month_name(accurate_bazi['lunar_month'])
            if accurate_bazi['is_leap_month']:
                lunar_month_name = f"闰{lunar_month_name}"
            
            prompt = f"""
{current_context}

我已经通过专业八字计算库（CNLunar）准确计算出您的八字信息：

**基本信息**：
- 公历出生：{birth_date} {birth_time}
- 农历出生：{accurate_bazi['lunar_year']}年{lunar_month_name}{self._get_lunar_day_name(accurate_bazi['lunar_day'])}
- 性别：{gender}
- 出生地：{location}

**八字排盘（经专业库准确计算）**：
- 年柱：{accurate_bazi['year_pillar']}
- 月柱：{accurate_bazi['month_pillar']}  
- 日柱：{accurate_bazi['day_pillar']}
- 时柱：{accurate_bazi['hour_pillar']}
- 完整八字：{accurate_bazi['full_bazi']}

请基于以上准确的八字信息，结合十大命理经典的理论，为我提供详细的专业分析：

1. **日主强弱分析**：分析日主在八字中的旺衰状态
2. **格局判断**：确定具体的命格类型（正官格、七杀格、财格等）
3. **用神选择**：根据格局和日主强弱确定用神
4. **大运流年**：分析当前大运和近期流年走势
5. **人生建议**：提供事业、财运、感情、健康等方面的具体建议

请确保分析的专业性和准确性。
"""
        else:
            # Fallback to standard prompt if CNLunar not available
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
def test_qji_cnlunar_engine():
    """Test Qji CNLunar engine"""
    try:
        engine = IndependentQjiCnlunarEngine()
        date_info = engine.get_current_date_info()
        print(f"✅ 日期信息获取成功: {date_info}")
        
        # Test bazi calculation
        if cnlunar_available:
            from datetime import datetime
            test_datetime = datetime(2026, 3, 10, 0, 38)
            test_bazi = engine.get_accurate_bazi(test_datetime)
            print(f"✅ 八字计算测试: {test_bazi}")
        
        response = engine.generate_response("你好，千机AI！")
        print(f"✅ 响应生成成功: {response[:50]}...")
        
        return "✅ Qji CNLunar引擎测试成功"
    except Exception as e:
        return f"❌ Qji CNLunar引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_qji_cnlunar_engine())