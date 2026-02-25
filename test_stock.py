#!/usr/bin/env python3
"""
Test stock skill functionality
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.skills.stock_skill import StockSkill

async def test_stock():
    """Test stock skill"""
    print("🔍 测试股票技能...")
    skill = StockSkill()
    
    try:
        result = await skill.execute("tesla stock price today")
        print(f"✅ 股票查询结果: {result}")
        return True
    except Exception as e:
        print(f"❌ 股票查询失败: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_stock())
    if success:
        print("🎉 股票技能测试通过！")
    else:
        print("💥 股票技能测试失败！")