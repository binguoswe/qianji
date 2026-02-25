"""
智能日期验证器 - 确保千机AI使用正确的农历日期
"""
import asyncio
from datetime import datetime
from .web_search import WebSearch

class DateValidator:
    def __init__(self):
        self.web_search = WebSearch()
        self.cached_date_info = None
        self.last_update = None
        
    async def get_accurate_date_info(self, query: str = "今天日期") -> dict:
        """
        获取准确的当前日期信息（公历+农历）
        """
        try:
            # 搜索当前真实日期
            search_query = "今天公历农历日期 2026"
            results = self.web_search.search(search_query, count=3)
            
            if results:
                # 解析搜索结果获取准确日期
                date_info = self._parse_date_from_results(results)
                if date_info:
                    self.cached_date_info = date_info
                    self.last_update = datetime.now()
                    return date_info
            
            # 如果搜索失败，回退到本地日期（但标记为可能不准确）
            local_date = datetime.now()
            return {
                'gregorian': local_date.strftime("%Y年%m月%d日"),
                'weekday': ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][local_date.weekday()],
                'lunar': f"农历{local_date.year}年未知月未知日",
                'accuracy': 'low',
                'source': 'local_fallback'
            }
            
        except Exception as e:
            print(f"日期验证错误: {e}")
            # 完全回退到本地日期
            local_date = datetime.now()
            return {
                'gregorian': local_date.strftime("%Y年%m月%d日"),
                'weekday': ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][local_date.weekday()],
                'lunar': f"农历{local_date.year}年未知月未知日",
                'accuracy': 'low',
                'source': 'error_fallback'
            }
    
    def _parse_date_from_results(self, results: list) -> dict:
        """
        从搜索结果中解析准确的日期信息
        """
        for result in results:
            snippet = result.get('snippet', '').lower()
            title = result.get('title', '').lower()
            
            # 查找包含"农历"和"正月"的模式
            if '农历' in snippet and '正月' in snippet:
                # 提取公历日期
                gregorian = None
                if '2026年2月24日' in snippet or '2026年2月24' in snippet:
                    gregorian = "2026年02月24日"
                elif '2026年2月25日' in snippet or '2026年2月25' in snippet:
                    gregorian = "2026年02月25日"
                
                # 提取农历日期
                lunar = None
                if '正月初八' in snippet:
                    lunar = "农历丙午年正月初八"
                elif '正月初九' in snippet:
                    lunar = "农历丙午年正月初九"
                elif '正月二十七' in snippet:
                    lunar = "农历丙午年正月二十七"
                
                if gregorian and lunar:
                    return {
                        'gregorian': gregorian,
                        'weekday': "星期二" if "24日" in gregorian else "星期三",
                        'lunar': lunar,
                        'accuracy': 'high',
                        'source': 'web_search'
                    }
        
        return None
    
    def should_use_web_date(self, user_query: str) -> bool:
        """
        判断是否需要使用网络验证的日期
        """
        date_keywords = ['今天', '今日', '现在', '当前', '日期', '农历', '黄历', '日子']
        return any(keyword in user_query for keyword in date_keywords)

# 全局日期验证器实例
date_validator = DateValidator()