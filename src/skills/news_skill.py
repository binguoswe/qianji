"""
News Skill for Qianji AI
Provides current news and trending topics
"""
import json
from datetime import datetime
from ..core.web_search import WebSearcher

class NewsSkill:
    def __init__(self):
        self.searcher = WebSearcher()
        self.name = "news"
        self.description = "获取当前新闻和热门话题"
        
    def can_handle(self, query: str) -> bool:
        """Check if this skill can handle the query"""
        news_keywords = ["新闻", "最新消息", "头条", "今日新闻", "热点", "趋势", "breaking news", "latest news"]
        return any(keyword in query.lower() for keyword in news_keywords)
    
    def execute(self, query: str, context: dict = None) -> dict:
        """
        Execute news search
        
        Args:
            query: User query
            context: Additional context (optional)
            
        Returns:
            dict with news results
        """
        try:
            # Extract specific news topic if mentioned
            news_topic = self._extract_news_topic(query)
            
            if news_topic:
                search_query = f"{news_topic} 最新新闻 2026"
            else:
                search_query = "今日热点新闻 2026"
            
            # Perform web search
            results = self.searcher.search(
                query=search_query,
                count=5,
                freshness="pd"  # Past 24 hours
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", ""),
                    "source": self._extract_source(result.get("url", ""))
                })
            
            return {
                "success": True,
                "skill": "news",
                "results": formatted_results,
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "skill": "news", 
                "error": str(e),
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_news_topic(self, query: str) -> str:
        """Extract specific news topic from query"""
        # Remove common news keywords
        clean_query = query
        news_keywords = ["新闻", "最新消息", "头条", "今日新闻", "热点", "趋势", "breaking news", "latest news"]
        
        for keyword in news_keywords:
            clean_query = clean_query.replace(keyword, "")
        
        # Remove question marks and extra spaces
        clean_query = clean_query.replace("？", "").replace("?", "").strip()
        
        return clean_query if clean_query else ""
    
    def _extract_source(self, url: str) -> str:
        """Extract source name from URL"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            # Remove www. and common prefixes
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except:
            return "Unknown"

# Test function
def test_news_skill():
    """Test the news skill"""
    skill = NewsSkill()
    
    # Test general news
    result = skill.execute("今日有什么新闻？")
    print(f"General news test: {'Success' if result['success'] else 'Failed'}")
    
    # Test specific topic
    result = skill.execute("科技新闻最新消息")
    print(f"Tech news test: {'Success' if result['success'] else 'Failed'}")
    
    return "News skill tests completed"

if __name__ == "__main__":
    print(test_news_skill())