#!/usr/bin/env python3
"""
Final test for enhanced Qji Max engine
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enhanced_engine():
    """Test the enhanced engine step by step"""
    print("🔍 测试增强版Qji Max引擎...")
    
    try:
        # Test 1: Import core modules
        print("1. 测试模块导入...")
        from src.core.web_search import WebSearch
        from src.core.skills import SkillManager
        from src.core.task_manager import TaskManager
        from src.core.enhanced_qji_engine import EnhancedQjiEngine
        print("✅ 所有核心模块导入成功！")
        
        # Test 2: Initialize components
        print("2. 测试组件初始化...")
        web_search = WebSearch()
        skill_manager = SkillManager()
        task_manager = TaskManager()
        print("✅ 所有组件初始化成功！")
        
        # Test 3: Initialize enhanced engine
        print("3. 测试增强引擎初始化...")
        engine = EnhancedQjiEngine()
        print("✅ 增强引擎初始化成功！")
        
        # Test 4: Basic response
        print("4. 测试基本响应...")
        response = engine.generate_response("你好，千机AI！")
        print(f"✅ 基本响应测试成功: {response[:50]}...")
        
        # Test 5: Web search capability
        print("5. 测试网络搜索能力...")
        search_results = web_search.search("今日黄历", count=2)
        print(f"✅ 网络搜索测试成功: {len(search_results)} 个结果")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_engine()
    if success:
        print("\n🎉 所有测试通过！增强版千机AI准备就绪！")
    else:
        print("\n💥 测试失败，请检查错误信息")
        sys.exit(1)