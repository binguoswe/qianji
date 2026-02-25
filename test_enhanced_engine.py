#!/usr/bin/env python3
"""
Test script for Enhanced Qji Max Engine
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_enhanced_engine():
    try:
        from src.core.enhanced_qji_engine import EnhancedQjiEngine
        print("✅ 正在初始化增强Qji Max引擎...")
        engine = EnhancedQjiEngine()
        print("✅ 增强Qji Max引擎初始化成功！")
        
        # Test basic functionality
        response = engine.generate_response("你好，千机AI！")
        print(f"✅ 基础功能测试成功: {response[:50]}...")
        
        # Test web search capability
        search_result = engine.search_web("今天天气如何")
        print(f"✅ 网络搜索功能测试成功: {search_result[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ 增强引擎测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_enhanced_engine()
    if success:
        print("\n🎉 千机AI增强版v1.1准备就绪！")
        print("新功能：")
        print("- 独立联网搜索能力")
        print("- 技能系统（插件化扩展）")
        print("- 多子任务并行处理")
        print("- 完全独立于OpenClaw")
    else:
        print("\n❌ 测试失败，请检查错误信息")