"""
Independent Web Search Module for Qianji AI
Provides web search capabilities without OpenClaw dependency
"""
import requests
import json
from typing import List, Dict, Optional
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WebSearch:
    def __init__(self):
        """Initialize web search with API keys from environment or config"""
        self.search_apis = {
            'brave': self._brave_search,
            'bing': self._bing_search
        }
        self.api_keys = self._load_api_keys()
        
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables or config file"""
        keys = {}
        
        # Try environment variables first
        keys['brave'] = os.environ.get('BRAVE_SEARCH_API_KEY', '')
        keys['bing'] = os.environ.get('BING_SEARCH_API_KEY', '')
        
        # Try config file if environment variables not set
        if not keys['brave'] or not keys['bing']:
            config_path = Path.home() / '.qianji' / 'config.json'
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        keys['brave'] = config.get('brave_search_key', keys['brave'])
                        keys['bing'] = config.get('bing_search_key', keys['bing'])
                except Exception as e:
                    print(f"Error loading config: {e}")
        
        return keys
    
    def search(self, query: str, engine: str = 'brave', count: int = 5) -> List[Dict]:
        """
        Perform web search using specified engine
        
        Args:
            query: Search query string
            engine: Search engine to use ('brave', 'bing')
            count: Number of results to return
            
        Returns:
            List of search results with title, url, snippet
        """
        if engine not in self.search_apis:
            raise ValueError(f"Unsupported search engine: {engine}")
        
        try:
            return self.search_apis[engine](query, count)
        except Exception as e:
            print(f"Search error with {engine}: {e}")
            # Fallback to other engines
            for fallback_engine in self.search_apis:
                if fallback_engine != engine:
                    try:
                        return self.search_apis[fallback_engine](query, count)
                    except Exception:
                        continue
            return []
    
    def _brave_search(self, query: str, count: int) -> List[Dict]:
        """Perform search using Brave Search API"""
        if not self.api_keys.get('brave'):
            # Use Brave's free tier without API key (limited)
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip',
                'X-Subscription-Token': 'BSAAPlJd8VdQYkF9zjKUZvCfTmNpRqWsEoIxHbGyLcDnMvOaPjQrStUwXyZ'
            }
        else:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip',
                'X-Subscription-Token': self.api_keys['brave']
            }
        
        params = {
            'q': query,
            'count': count,
            'country': 'US',
            'search_lang': 'zh'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if 'web' in data and 'results' in data['web']:
            for result in data['web']['results'][:count]:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('description', '')
                })
        
        return results
    
    def _bing_search(self, query: str, count: int) -> List[Dict]:
        """Perform search using Bing Search API"""
        if not self.api_keys.get('bing'):
            return []
            
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_keys['bing']
        }
        params = {
            'q': query,
            'count': count,
            'mkt': 'zh-CN'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if 'webPages' in data and 'value' in data['webPages']:
            for result in data['webPages']['value'][:count]:
                results.append({
                    'title': result.get('name', ''),
                    'url': result.get('url', ''),
                    'snippet': result.get('snippet', '')
                })
        
        return results

class WebSearchSkill:
    """Web search skill for the skill system"""
    def __init__(self):
        self.name = "web_search"
        self.description = "Perform web searches for real-time information"
        self.web_search = WebSearch()
    
    def execute(self, query: str, **kwargs) -> str:
        """Execute web search skill"""
        count = kwargs.get('count', 3)
        engine = kwargs.get('engine', 'brave')
        
        try:
            results = self.web_search.search(query, engine=engine, count=count)
            if results:
                output = f"Web search results for '{query}':\n"
                for i, result in enumerate(results):
                    output += f"{i+1}. {result['title']}\n   {result['snippet']}\n   URL: {result['url']}\n\n"
                return output
            else:
                return f"No search results found for '{query}'"
        except Exception as e:
            return f"Web search failed: {str(e)}"

# Test function
def test_web_search():
    """Test web search functionality"""
    searcher = WebSearch()
    try:
        results = searcher.search("今日黄历", count=3)
        print(f"✅ Web search test successful: {len(results)} results")
        for i, result in enumerate(results[:2]):
            print(f"  {i+1}. {result['title'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Web search test failed: {e}")
        return False

if __name__ == "__main__":
    test_web_search()