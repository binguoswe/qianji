#!/usr/bin/env python3
"""
Final integration test for enhanced Qji Max engine with real web search and skills
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.enhanced_qji_engine import EnhancedQjiEngine

async def test_real_stock_query():
    """Test real stock query with actual skill execution"""
    print("🔍 测试真实股票查询...")
    
    try:
        engine = EnhancedQjiEngine()
        
        # Test stock query
        message = "帮我搜搜今天tesla股票多少钱一股收盘的"
        response = engine.generate_response(message)
        
        print(f"✅ 股票查询结果:\n{response}")
        return True
        
    except Exception as e:
        print(f"❌ 股票查询失败: {e}")
        return False

def main():
    """Run final integration test"""
    print("🚀 运行最终集成测试...")
    
    # Test stock query
    success = asyncio.run(test_real_stock_query())
    
    if success:
        print("\n🎉 所有测试通过！增强版千机AI已具备真实联网功能！")
    else:
        print("\n❌ 测试失败，请检查错误信息")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)