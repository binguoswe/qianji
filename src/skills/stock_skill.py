"""
Stock Price Skill for Qianji AI
Provides real-time stock price information
"""
import requests
import json
from typing import Dict, Any

class StockSkill:
    def __init__(self):
        self.name = "stock"
        self.description = "Get real-time stock prices and financial information"
    
    async def execute(self, query: str) -> str:
        """
        Execute stock price query
        """
        try:
            # Extract stock symbol from query
            stock_symbol = self._extract_stock_symbol(query)
            if not stock_symbol:
                return "请提供具体的股票代码或公司名称，例如 'TSLA' 或 '特斯拉'"
            
            # Get stock price from Yahoo Finance API (free)
            price_data = self._get_stock_price(stock_symbol)
            
            if price_data:
                return f"📊 **{price_data['symbol']} ({price_data['name']})**\n\n" \
                       f"💰 当前价格: ${price_data['price']:.2f}\n" \
                       f"📈 日涨跌幅: {price_data['change']:.2f}%\n" \
                       f"📅 更新时间: {price_data['timestamp']}\n\n" \
                       f"数据来源: Yahoo Finance"
            else:
                return f"抱歉，无法获取 {stock_symbol} 的实时股价信息。"
                
        except Exception as e:
            print(f"Stock skill error: {e}")
            return "股票查询服务暂时不可用，请稍后重试。"
    
    def _extract_stock_symbol(self, query: str) -> str:
        """Extract stock symbol from query"""
        # Simple extraction - in production, use NLP
        symbols = {
            'tesla': 'TSLA',
            '特斯拉': 'TSLA',
            'apple': 'AAPL',
            '苹果': 'AAPL',
            'microsoft': 'MSFT',
            '微软': 'MSFT',
            'google': 'GOOGL',
            '谷歌': 'GOOGL'
        }
        
        query_lower = query.lower()
        for keyword, symbol in symbols.items():
            if keyword in query_lower:
                return symbol
        
        # If no match, return the query as-is (might be a symbol)
        return query.strip().upper()
    
    def _get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Get stock price from Yahoo Finance"""
        try:
            # Yahoo Finance API endpoint
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return None
            
            data = response.json()
            
            if 'chart' not in data or 'result' not in data['chart']:
                return None
            
            result = data['chart']['result'][0]
            meta = result['meta']
            timestamp = result['timestamp'][-1]
            close_price = result['indicators']['quote'][0]['close'][-1]
            open_price = result['indicators']['quote'][0]['open'][-1]
            
            change_percent = ((close_price - open_price) / open_price) * 100
            
            return {
                'symbol': symbol,
                'name': meta.get('shortName', symbol),
                'price': close_price,
                'change': change_percent,
                'timestamp': self._format_timestamp(timestamp)
            }
            
        except Exception as e:
            print(f"Yahoo Finance API error: {e}")
            return None
    
    def _format_timestamp(self, timestamp: int) -> str:
        """Format timestamp to readable date"""
        from datetime import datetime
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")

# Test function
def test_stock_skill():
    """Test stock skill functionality"""
    skill = StockSkill()
    result = skill.execute("特斯拉股票价格")
    print(f"Stock skill test result: {result}")

if __name__ == "__main__":
    test_stock_skill()