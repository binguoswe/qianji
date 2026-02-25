"""
Free Web Search Module for Qianji AI
Uses DuckDuckGo and other free search engines without API keys
"""
import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Optional
import time
import re

class FreeWebSearch:
    def __init__(self):
        """Initialize free web search with no API dependencies"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def search(self, query: str, count: int = 5) -> List[Dict]:
        """
        Perform free web search using DuckDuckGo
        No API key required!
        """
        try:
            return self._duckduckgo_search(query, count)
        except Exception as e:
            print(f"DDG search failed: {e}")
            # Fallback to simple Bing search
            try:
                return self._simple_bing_search(query, count)
            except Exception as e2:
                print(f"Bing fallback failed: {e2}")
                return []
    
    def _duckduckgo_search(self, query: str, count: int) -> List[Dict]:
        """Search using DuckDuckGo HTML interface"""
        url = "https://html.duckduckgo.com/html/"
        data = {
            'q': query,
            'kl': 'us-en'
        }
        
        response = self.session.post(url, data=data, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Parse DDG results
        result_divs = soup.find_all('div', class_='result')
        for div in result_divs[:count]:
            title_elem = div.find('a', class_='result__a')
            snippet_elem = div.find('a', class_='result__snippet')
            url_elem = div.find('a', class_='result__url')
            
            if title_elem:
                title = title_elem.get_text().strip()
                url = title_elem.get('href', '')
                snippet = snippet_elem.get_text().strip() if snippet_elem else ''
                
                # Clean up URL
                if url.startswith('/'):
                    url = f"https://duckduckgo.com{url}"
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })
        
        return results[:count]
    
    def _simple_bing_search(self, query: str, count: int) -> List[Dict]:
        """Simple Bing search using public interface"""
        url = f"https://www.bing.com/search"
        params = {'q': query}
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Parse Bing results
        result_list = soup.find('ol', {'id': 'b_results'})
        if result_list:
            li_items = result_list.find_all('li', class_='b_algo')
            for li in li_items[:count]:
                title_elem = li.find('h2')
                desc_elem = li.find('p')
                
                if title_elem and title_elem.find('a'):
                    title = title_elem.get_text().strip()
                    url = title_elem.find('a').get('href', '')
                    snippet = desc_elem.get_text().strip() if desc_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
        
        return results[:count]

# Test function
def test_free_search():
    """Test free web search functionality"""
    searcher = FreeWebSearch()
    try:
        results = searcher.search("今日新闻", count=3)
        print(f"✅ Free search test successful: {len(results)} results")
        for i, result in enumerate(results[:2]):
            print(f"  {i+1}. {result['title'][:50]}...")
        return True
    except Exception as e:
        print(f"❌ Free search test failed: {e}")
        return False

if __name__ == "__main__":
    test_free_search()