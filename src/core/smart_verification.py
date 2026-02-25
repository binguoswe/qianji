"""
Smart Verification Module for Qianji AI
Adds verification prompts for critical information like dates, numbers, etc.
"""
import re

class SmartVerification:
    def __init__(self):
        self.critical_keywords = [
            '农历', '阴历', '阳历', '公历', '日期', '今天', '明日', '昨日',
            '正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '腊月',
            '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
            '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
            '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
        ]
    
    def needs_verification(self, response: str) -> bool:
        """Check if response contains critical information that needs verification"""
        return any(keyword in response for keyword in self.critical_keywords)
    
    def add_verification_prompt(self, response: str) -> str:
        """Add verification prompt to response"""
        if self.needs_verification(response):
            verification_prompt = "\n\n💡 **信息验证提示**: 以上农历日期信息基于实时网络搜索。为了确保准确性，建议您也可以通过权威万年历网站（如中国科学院紫金山天文台发布的农历数据）进行交叉验证。"
            return response + verification_prompt
        return response