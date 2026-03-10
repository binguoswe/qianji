"""
Simple Date Handler for Qianji AI
Provides real-time date and lunar conversion without external dependencies
"""
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Add project root to path to import lunar calculator
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

try:
    from lunardate import LunarDate
except ImportError:
    print("Warning: lunardate not available, date handling will be limited")
    LunarDate = None

class SimpleDateHandler:
    def __init__(self):
        self.has_lunar_support = LunarDate is not None
    
    def get_current_datetime(self) -> datetime:
        """Get current system datetime"""
        return datetime.now()
    
    def get_current_date_context(self) -> Dict[str, Any]:
        """Get comprehensive current date context"""
        now = self.get_current_datetime()
        
        context = {
            'current_datetime': now,
            'current_date': now.strftime("%Y-%m-%d"),
            'current_date_chinese': now.strftime("%Y年%m月%d日"),
            'current_weekday': ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()],
            'current_year': now.year,
            'current_month': now.month,
            'current_day': now.day,
            'current_hour': now.hour,
            'current_minute': now.minute
        }
        
        # Add lunar date if available
        if self.has_lunar_support:
            try:
                lunar_date = LunarDate.fromSolarDate(now.year, now.month, now.day)
                context['lunar_year'] = lunar_date.year
                context['lunar_month'] = lunar_date.month
                context['lunar_day'] = lunar_date.day
                context['is_leap_month'] = getattr(lunar_date, 'isLeapMonth', False)
                context['lunar_date_chinese'] = self._format_lunar_date(lunar_date)
            except Exception as e:
                print(f"Warning: Lunar date conversion failed: {e}")
                context['lunar_date_chinese'] = "农历日期获取失败"
        else:
            context['lunar_date_chinese'] = "农历功能未启用"
        
        return context
    
    def _format_lunar_date(self, lunar_date) -> str:
        """Format lunar date in Chinese"""
        # 农历月份名称
        lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                       "七月", "八月", "九月", "十月", "冬月", "腊月"]
        # 农历日名称  
        lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                     "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                     "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
        
        month_name = lunar_months[lunar_date.month - 1]
        if hasattr(lunar_date, 'isLeapMonth') and lunar_date.isLeapMonth:
            month_name = f"闰{month_name}"
        
        day_name = lunar_days[lunar_date.day - 1] if 1 <= lunar_date.day <= 30 else f"{lunar_date.day}日"
        
        return f"{lunar_date.year}年{month_name}{day_name}"

# Test function
def test_simple_date_handler():
    """Test simple date handler"""
    handler = SimpleDateHandler()
    context = handler.get_current_date_context()
    print("Current date context:")
    for key, value in context.items():
        print(f"  {key}: {value}")
    return context

if __name__ == "__main__":
    test_simple_date_handler()