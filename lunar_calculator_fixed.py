#!/usr/bin/env python3
"""
农历计算器 - 修复版本
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

try:
    from lunardate import LunarDate
    from cnlunar import Lunar
except ImportError:
    print("错误：请先安装依赖库：pip install lunardate cnlunar")
    sys.exit(1)

# 干支纪年
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ZODIAC = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 农历月份名称
LUNAR_MONTHS = ["正月", "二月", "三月", "四月", "五月", "六月", 
                "七月", "八月", "九月", "十月", "冬月", "腊月"]

# 农历日名称
LUNAR_DAYS = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
              "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
              "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]

class LunarCalculator:
    """农历计算器核心类"""
    
    def get_ganzhi_year(self, year: int) -> str:
        """获取干支纪年"""
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        return f"{TIAN_GAN[gan_index]}{DI_ZHI[zhi_index]}"
    
    def get_zodiac(self, year: int) -> str:
        """获取生肖"""
        return ZODIAC[(year - 1900) % 12]
    
    def get_lunar_month_name(self, month: int, is_leap: bool = False) -> str:
        """获取农历月份名称"""
        if 1 <= month <= 12:
            name = LUNAR_MONTHS[month - 1]
            return f"闰{name}" if is_leap else name
        return f"{month}月"
    
    def get_lunar_day_name(self, day: int) -> str:
        """获取农历日名称"""
        if 1 <= day <= 30:
            return LUNAR_DAYS[day - 1]
        return f"{day}日"
    
    def get_festival(self, lunar_month: int, lunar_day: int) -> Optional[str]:
        """获取传统节日"""
        festivals = {
            (1, 1): "春节",
            (1, 15): "元宵节",
            (5, 5): "端午节",
            (7, 7): "七夕节",
            (7, 15): "中元节",
            (8, 15): "中秋节",
            (9, 9): "重阳节",
            (12, 8): "腊八节",
            (12, 23): "小年",
            (12, 30): "除夕"
        }
        return festivals.get((lunar_month, lunar_day))
    
    def solar_to_lunar(self, solar_date: str) -> Dict[str, Any]:
        """公历转农历"""
        try:
            year, month, day = map(int, solar_date.split('-'))
            
            # 使用lunardate库进行转换
            lunar_date = LunarDate.fromSolarDate(year, month, day)
            
            # 使用cnlunar获取更详细信息 - 需要完整日期时间
            dt = datetime(year, month, day)
            lunar_info = Lunar(dt)
            
            result = {
                "solar_date": solar_date,
                "lunar_year": lunar_date.year,
                "lunar_month": lunar_date.month,
                "lunar_day": lunar_date.day,
                "is_leap": lunar_date.isLeap,
                "lunar_month_name": self.get_lunar_month_name(lunar_date.month, lunar_date.isLeap),
                "lunar_day_name": self.get_lunar_day_name(lunar_date.day),
                "ganzhi_year": self.get_ganzhi_year(lunar_date.year),
                "zodiac": self.get_zodiac(lunar_date.year),
                "festival": self.get_festival(lunar_date.month, lunar_date.day),
                "lunar_full": str(lunar_info)
            }
            
            return result
            
        except Exception as e:
            return {"error": f"日期转换失败: {str(e)}"}
    
    def lunar_to_solar(self, lunar_year: int, lunar_month: int, lunar_day: int, 
                      is_leap: bool = False) -> Dict[str, Any]:
        """农历转公历"""
        try:
            # 使用lunardate库进行转换
            lunar_date = LunarDate(lunar_year, lunar_month, lunar_day, is_leap)
            solar_date = lunar_date.toSolarDate()
            
            solar_str = solar_date.strftime("%Y-%m-%d")
            
            result = {
                "lunar_date": f"{lunar_year}年{self.get_lunar_month_name(lunar_month, is_leap)}{self.get_lunar_day_name(lunar_day)}",
                "solar_date": solar_str,
                "ganzhi_year": self.get_ganzhi_year(lunar_year),
                "zodiac": self.get_zodiac(lunar_year),
                "festival": self.get_festival(lunar_month, lunar_day)
            }
            
            return result
            
        except Exception as e:
            return {"error": f"农历转换失败: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description='农历查询引擎（修复版）')
    parser.add_argument('--solar', type=str, help='公历日期: 2026-02-13')
    parser.add_argument('--lunar', type=str, help='农历日期: 2026-07-23 表示农历二零二六年七月廿三')
    parser.add_argument('--leap', type=bool, default=False, help='是否为闰月')
    
    args = parser.parse_args()
    
    calculator = LunarCalculator()
    
    if args.solar:
        result = calculator.solar_to_lunar(args.solar)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.lunar:
        try:
            lunar_year, lunar_month, lunar_day = map(int, args.lunar.split('-'))
            result = calculator.lunar_to_solar(lunar_year, lunar_month, lunar_day, args.leap)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except ValueError:
            print(json.dumps({"error": "农历日期格式错误，请使用YYYY-MM-DD格式"}, ensure_ascii=False))
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()