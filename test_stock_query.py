#!/usr/bin/env python3
"""
Test stock query with enhanced Qji Max engine
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.enhanced_qji_engine import EnhancedQjiEngine

def test_stock_query():
    """Test stock query functionality"""
    print("🔍 测试股票查询功能...")
    
    try:
        # Initialize engine
        engine = EnhancedQjiEngine()
        
        # Test stock query
        query = "帮我搜搜今天tesla股票多少钱一股收盘的"
        response = engine.generate_response(query)
        
        print("✅ 完整查询结果:")
        print(response)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_stock_query()
    if success:
        print("\n🎉 股票查询测试完成！")
    else:
        print("\n❌ 股票查询测试失败！")