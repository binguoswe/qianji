"""
Weather Skill for Qji Max
Provides weather forecasting and current conditions
"""
import requests
import json
from datetime import datetime

class WeatherSkill:
    def __init__(self):
        self.name = "weather"
        self.description = "Get current weather and forecasts"
        self.api_key = None  # Will be set by the main engine
        
    def can_handle(self, query):
        """Check if this skill can handle the query"""
        weather_keywords = ["天气", "weather", "temperature", "气温", "forecast", "预报", "rain", "雨", "snow", "雪"]
        return any(keyword in query.lower() for keyword in weather_keywords)
    
    def execute(self, query, context=None):
        """Execute weather query"""
        if not self.api_key:
            return "Weather API key not configured"
            
        # Extract location from query
        location = self._extract_location(query)
        if not location:
            location = "Beijing"  # Default location
            
        try:
            # Get current weather
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric&lang=zh_cn"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    "location": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
                
                return self._format_weather_response(weather_info)
            else:
                return f"无法获取 {location} 的天气信息"
                
        except Exception as e:
            return f"天气查询出错: {str(e)}"
    
    def _extract_location(self, query):
        """Extract location from query (simple implementation)"""
        # This is a simplified version - in real implementation, use NLP
        locations = ["北京", "上海", "广州", "深圳", "杭州", "成都", "西安", "武汉", "南京", "重庆"]
        for loc in locations:
            if loc in query:
                return loc
        return None
    
    def _format_weather_response(self, weather_info):
        """Format weather response for Qji Max"""
        return f"""🌤️ **{weather_info['location']} 当前天气**

温度: {weather_info['temperature']}°C
天气: {weather_info['description']}
湿度: {weather_info['humidity']}%
风速: {weather_info['wind_speed']} m/s

注意：以上信息仅供参考，实际天气可能有所变化。"""