"""
Intelligent Decision Engine for Qianji AI
Determines when to use web search vs rely on internal knowledge
"""
import re
from datetime import datetime
from typing import Dict, List, Tuple

class IntelligentDecisionEngine:
    def __init__(self):
        # Keywords that indicate need for real-time information
        self.real_time_keywords = [
            '今天', '今日', '现在', '当前', '最新', '实时', '最近', '刚刚',
            '新闻', '天气', '股价', '股票', '汇率', '疫情', '事件',
            '农历', '阴历', '黄历', '万年历', '老黄历', '日历',
            '几号', '星期几', '时间', '日期', '日子'
        ]
        
        # Keywords that indicate static knowledge
        self.static_knowledge_keywords = [
            '什么是', '为什么', '如何', '原理', '理论', '概念',
            '历史', '古代', '传统', '经典', '书籍', '作者',
            '数学', '物理', '化学', '生物', '地理'
        ]
        
        # High-confidence domains (no search needed)
        self.high_confidence_domains = [
            'basic_math', 'general_knowledge', 'classic_literature',
            'historical_facts', 'scientific_principles'
        ]
        
        # Low-confidence domains (search recommended)
        self.low_confidence_domains = [
            'current_events', 'financial_data', 'weather',
            'lunar_calendar', 'daily_horoscope', 'stock_prices'
        ]
    
    def should_enable_search(self, message: str, conversation_history: List[Dict] = None) -> Tuple[bool, str]:
        """
        Determine whether to enable web search for a given query
        
        Returns:
            Tuple[bool, str]: (should_search, reason)
        """
        # Check for explicit real-time indicators
        if self._has_real_time_indicators(message):
            return True, "Query contains real-time indicators (today, current, etc.)"
        
        # Check for date/calendar related queries
        if self._is_date_or_calendar_query(message):
            return True, "Query involves date/calendar calculation requiring verification"
        
        # Check for financial or market data
        if self._is_financial_query(message):
            return True, "Query involves financial/market data requiring real-time info"
        
        # Check for weather queries
        if self._is_weather_query(message):
            return True, "Query involves weather requiring real-time data"
        
        # Check for news/current events
        if self._is_news_query(message):
            return True, "Query involves current events/news requiring real-time info"
        
        # Check if model confidence is likely low
        if self._likely_low_confidence(message):
            return True, "Query likely requires external verification for accuracy"
        
        # Default: no search needed for general knowledge
        return False, "Query appears to be general knowledge that can be answered from internal knowledge"
    
    def _has_real_time_indicators(self, message: str) -> bool:
        """Check if message contains real-time indicators"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.real_time_keywords)
    
    def _is_date_or_calendar_query(self, message: str) -> bool:
        """Check if query involves date/calendar calculations"""
        date_patterns = [
            r'今天.*?农历',
            r'农历.*?今天', 
            r'几月几日',
            r'正月.*?\d+',
            r'腊月.*?\d+',
            r'黄历',
            r'万年历',
            r'老黄历',
            r'日历',
            r'几号',
            r'星期几'
        ]
        
        for pattern in date_patterns:
            if re.search(pattern, message):
                return True
        return False
    
    def _is_financial_query(self, message: str) -> bool:
        """Check if query involves financial data"""
        financial_keywords = ['股票', '股价', '汇率', '基金', '投资', '理财', '银行', '利率']
        return any(keyword in message for keyword in financial_keywords)
    
    def _is_weather_query(self, message: str) -> bool:
        """Check if query involves weather"""
        weather_keywords = ['天气', '气温', '温度', '下雨', '晴天', '预报', '气候']
        return any(keyword in message for keyword in weather_keywords)
    
    def _is_news_query(self, message: str) -> bool:
        """Check if query involves news/current events"""
        news_keywords = ['新闻', '最新消息', '头条', '事件', '发生', '最近', '刚刚']
        return any(keyword in message for keyword in news_keywords)
    
    def _likely_low_confidence(self, message: str) -> bool:
        """Check if query likely requires external verification"""
        # Queries asking for specific numbers, dates, or facts that could be outdated
        low_confidence_patterns = [
            r'\d{4}年.*?是.*?年',
            r'今年.*?是.*?年',
            r'.*?多少.*?',
            r'.*?几.*?',
            r'确认.*?',
            r'验证.*?'
        ]
        
        for pattern in low_confidence_patterns:
            if re.search(pattern, message):
                return True
        return False
    
    def get_search_strategy(self, message: str) -> str:
        """Determine search strategy based on query type"""
        if self._is_date_or_calendar_query(message):
            return "max"  # Most comprehensive search for accuracy
        elif self._is_financial_query(message) or self._is_weather_query(message):
            return "balanced"  # Good balance of speed and accuracy
        else:
            return "fast"  # Quick search for general verification

# Test function
def test_intelligent_decision():
    """Test the intelligent decision engine"""
    engine = IntelligentDecisionEngine()
    
    test_queries = [
        "今天农历是多少？",
        "什么是量子力学？", 
        "苹果股票现在多少钱？",
        "北京今天天气如何？",
        "《三命通会》是谁写的？",
        "2026年是什么生肖年？"
    ]
    
    results = []
    for query in test_queries:
        should_search, reason = engine.should_enable_search(query)
        strategy = engine.get_search_strategy(query) if should_search else "none"
        results.append(f"Query: '{query}'\n  Search: {should_search}\n  Reason: {reason}\n  Strategy: {strategy}\n")
    
    return "\n".join(results)

if __name__ == "__main__":
    print(test_intelligent_decision())