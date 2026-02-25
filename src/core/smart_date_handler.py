"""
Smart Date Handler for Qianji AI
Automatically validates and corrects date-related queries using web search
"""
import requests
import json
from datetime import datetime
from .web_search import WebSearch

class SmartDateHandler:
    def __init__(self):
        self.web_search = WebSearch()
        self.date_keywords = ['今天', '今日', '现在', '当前', '日期', '日子', '农历', '阴历', '阳历', '黄历', '星期']
    
    def should_handle_date_query(self, message: str) -> bool:
        """Check if message requires date validation"""
        return any(keyword in message for keyword in self.date_keywords)
    
    def get_accurate_date_info(self, message: str) -> str:
        """
        Get accurate date information by searching the web
        Returns formatted date context string
        """
        try:
            # Get current date for search query
            now = datetime.now()
            current_date_str = now.strftime("%Y年%m月%d日")
            
            # Create search query
            search_query = f"今天农历日期 {current_date_str} 农历"
            
            # Perform web search
            results = self.web_search.search(search_query, count=3)
            
            if results:
                # Extract date information from search results
                date_info = "【联网验证的真实日期信息】\n"
                for i, result in enumerate(results[:2]):
                    title = result.get('title', '')
                    snippet = result.get('snippet', '')
                    if title or snippet:
                        date_info += f"- 来源{i+1}: {title}\n  内容: {snippet}\n"
                return date_info
            
            # Fallback to basic date info
            weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
            return f"【基础日期信息】\n- 公历日期: {current_date_str}\n- 星期: {weekday}\n- 注意: 未获取到农历信息，请以权威黄历为准"
            
        except Exception as e:
            print(f"Date validation error: {e}")
            # Return safe fallback
            now = datetime.now()
            weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
            current_date_str = now.strftime("%Y年%m月%d日")
            return f"【日期信息（本地计算）】\n- 公历日期: {current_date_str}\n- 星期: {weekday}\n- 农历日期: 请查询权威黄历确认"
    
    def enhance_prompt_with_date_context(self, original_prompt: str, message: str) -> str:
        """Enhance prompt with accurate date context"""
        if self.should_handle_date_query(message):
            date_context = self.get_accurate_date_info(message)
            enhanced_prompt = f"""{original_prompt}

【重要日期上下文】
{date_context}

请基于以上准确的日期信息回答用户问题，特别是涉及农历、黄历、运势等内容时。
"""
            return enhanced_prompt
        return original_prompt

# Test function
def test_smart_date_handler():
    """Test smart date handler"""
    handler = SmartDateHandler()
    
    # Test date query detection
    test_message = "今天是什么日子？"
    should_handle = handler.should_handle_date_query(test_message)
    print(f"Should handle '{test_message}': {should_handle}")
    
    # Test date info retrieval
    if should_handle:
        date_info = handler.get_accurate_date_info(test_message)
        print(f"Date info:\n{date_info}")
    
    return "Smart date handler test completed"

if __name__ == "__main__":
    print(test_smart_date_handler())