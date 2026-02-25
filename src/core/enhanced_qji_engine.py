"""
Enhanced Qji Max Engine with Web Search, Skills, Parallel Task Processing, and Date Validation
"""
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .web_search import WebSearch
from .skills import SkillManager
from .task_manager import TaskManager
from .independent_qwen import call_qwen_max_api
from .date_validator import DateValidator

class EnhancedQjiEngine:
    def __init__(self):
        """Initialize enhanced Qji Max engine with all capabilities"""
        print("🚀 正在初始化增强版Qji Max引擎...")
        
        # Initialize core components
        self.web_search = WebSearch()
        self.skill_manager = SkillManager()
        self.task_manager = TaskManager()
        self.qwen_engine = call_qwen_max_api
        self.date_validator = DateValidator()
        
        print("✅ 增强版Qji Max引擎初始化完成！")
    
    async def generate_response_async(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate response with web search, skills, and parallel processing capabilities
        """
        if conversation_history is None:
            conversation_history = []
        
        # Check if message contains date-related queries
        needs_date_validation = self._contains_date_query(message)
        accurate_date_context = ""
        
        if needs_date_validation:
            try:
                accurate_date_context = await self.date_validator.get_accurate_date_info()
            except Exception as e:
                print(f"日期验证失败: {e}")
                # Fallback to local date
                current_date = datetime.now().strftime("%Y年%m月%d日")
                current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][datetime.now().weekday()]
                accurate_date_context = f"当前日期: {current_date}, {current_weekday}"
        
        # Analyze message to determine required capabilities
        analysis = await self._analyze_message_requirements(message)
        
        # Prepare context based on analysis
        context = await self._prepare_context(analysis, message, conversation_history)
        
        # Build final prompt with accurate date info
        if needs_date_validation and accurate_date_context:
            date_info = accurate_date_context
        else:
            current_date = datetime.now().strftime("%Y年%m月%d日")
            current_weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][datetime.now().weekday()]
            date_info = f"{current_date}，{current_weekday}"
        
        qji_context = f"""
你是一个AI助手，名为千机AI（Qji AI）。当前准确日期信息：{date_info}

你的特点：
1. **通用AI能力**：正常回答各种日常问题
2. **命理风水专长**：深度专业知识  
3. **联网搜索能力**：可以获取实时信息
4. **多任务处理**：可以并行处理复杂请求
5. **日期准确性**：总是使用经过验证的准确日期

上下文信息：
{context}

请根据用户问题和上下文提供最佳回答。特别注意：如果涉及日期、农历、黄历等信息，必须基于提供的准确日期信息回答。
"""
        
        full_prompt = f"{qji_context}\n\n用户问题: {message}"
        
        try:
            response = self.qwen_engine(full_prompt, conversation_history)
            return response
        except Exception as e:
            print(f"生成响应错误: {e}")
            return "抱歉，处理您的请求时出现了问题。"
    
    def _contains_date_query(self, message: str) -> bool:
        """Check if message contains date-related queries"""
        date_keywords = [
            '今天', '今日', '现在', '当前', '日期', '日子', '农历', '阳历', 
            '公历', '黄历', '运势', '星期', '月份', '年份', '时间'
        ]
        return any(keyword in message for keyword in date_keywords)
    
    async def _analyze_message_requirements(self, message: str) -> Dict[str, Any]:
        """
        Analyze message to determine what capabilities are needed
        """
        requirements = {
            'needs_web_search': False,
            'needs_skills': [],
            'needs_parallel_tasks': False,
            'search_query': '',
            'skill_requests': []
        }
        
        # Check for web search needs
        search_keywords = ['今天', '最新', '新闻', '天气', '黄历', '实时', '现在', '当前']
        if any(keyword in message for keyword in search_keywords):
            requirements['needs_web_search'] = True
            requirements['search_query'] = message
        
        # Check for skill needs
        if '天气' in message or 'weather' in message.lower():
            requirements['needs_skills'].append('weather')
            requirements['skill_requests'].append({'skill': 'weather', 'query': message})
        
        if '新闻' in message or 'news' in message.lower():
            requirements['needs_skills'].append('news')
            requirements['skill_requests'].append({'skill': 'news', 'query': message})
        
        if '八字' in message or '命理' in message or 'bazi' in message.lower():
            requirements['needs_skills'].append('bazi')
            requirements['skill_requests'].append({'skill': 'bazi', 'query': message})
        
        if '股票' in message or '股价' in message or 'stock' in message.lower() or 'price' in message.lower():
            requirements['needs_skills'].append('stock')
            requirements['skill_requests'].append({'skill': 'stock', 'query': message})
        
        # Check for complex multi-task needs
        if len(requirements['skill_requests']) > 1:
            requirements['needs_parallel_tasks'] = True
        
        return requirements
    
    async def _prepare_context(self, analysis: Dict[str, Any], message: str, history: List[Dict[str, str]]) -> str:
        """
        Prepare context by executing required capabilities
        """
        context_parts = []
        
        # Execute web search if needed
        if analysis['needs_web_search']:
            try:
                search_results = self.web_search.search(analysis['search_query'], count=3)
                if search_results:
                    context_parts.append("【网络搜索结果】")
                    for i, result in enumerate(search_results[:2]):
                        context_parts.append(f"{i+1}. {result['title']}: {result['snippet']}")
            except Exception as e:
                print(f"搜索执行错误: {e}")
        
        # Execute skills if needed
        if analysis['needs_skills']:
            for skill_request in analysis['skill_requests']:
                try:
                    skill_result = await self.skill_manager.execute_skill(
                        skill_request['skill'], 
                        query=skill_request['query']
                    )
                    if skill_result:
                        context_parts.append(f"【{skill_request['skill']}技能结果】")
                        context_parts.append(skill_result)
                except Exception as e:
                    print(f"技能执行错误: {e}")
        
        return "\n".join(context_parts) if context_parts else "无额外上下文信息"
    
    def generate_response(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Synchronous wrapper for async generate_response
        """
        return asyncio.run(self.generate_response_async(message, conversation_history))
    
    def analyze_bazi(self, birth_date: str, birth_time: str, gender: str, location: str) -> str:
        """
        Analyze bazi with enhanced capabilities
        """
        prompt = f"""
请为我详细分析这个八字：
- 出生日期: {birth_date}
- 出生时间: {birth_time}  
- 性别: {gender}
- 出生地点: {location}

需要包含以下内容：
1. 四柱八字排盘（年柱、月柱、日柱、时柱）
2. 日主强弱分析
3. 格局判断和用神选择
4. 大运流年分析
5. 具体的人生建议（事业、财运、感情、健康）

请基于十大命理经典的理论进行专业分析。
"""
        
        try:
            response = self.qwen_engine(prompt, [])
            return response
        except Exception as e:
            print(f"八字分析错误: {e}")
            return "抱歉，八字分析时出现了问题。"

# Test function
def test_enhanced_engine():
    """Test enhanced Qji Max engine"""
    try:
        engine = EnhancedQjiEngine()
        response = engine.generate_response("今天是农历几号？")
        return f"✅ 增强引擎测试成功: {response[:50]}..."
    except Exception as e:
        return f"❌ 增强引擎测试失败: {e}"

if __name__ == "__main__":
    print(test_enhanced_engine())