#!/usr/bin/env python3
"""
简化版农历转换器 - 专为千机项目设计
"""

import sys
import json
from datetime import datetime
from lunardate import LunarDate

def solar_to_lunar(solar_date_str):
    """公历转农历"""
    try:
        year, month, day = map(int, solar_date_str.split('-'))
        lunar_date = LunarDate.fromSolarDate(year, month, day)
        
        # 农历月份名称
        lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                       "七月", "八月", "九月", "十月", "冬月", "腊月"]
        lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                     "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                     "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
        
        month_name = lunar_months[lunar_date.month - 1]
        day_name = lunar_days[lunar_date.day - 1]
        
        # 干支纪年（简化）
        tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        zodiac = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        
        gan_index = (lunar_date.year - 4) % 10
        zhi_index = (lunar_date.year - 4) % 12
        ganzhi_year = f"{tian_gan[gan_index]}{di_zhi[zhi_index]}"
        zodiac_animal = zodiac[(lunar_date.year - 1900) % 12]
        
        return {
            "solar_date": solar_date_str,
            "lunar_date": f"{lunar_date.year}年{month_name}{day_name}",
            "ganzhi_year": ganzhi_year,
            "zodiac": zodiac_animal,
            "lunar_year": lunar_date.year,
            "lunar_month": lunar_date.month,
            "lunar_day": lunar_date.day
        }
    except Exception as e:
        return {"error": f"转换失败: {str(e)}"}

def lunar_to_solar(lunar_year, lunar_month, lunar_day):
    """农历转公历"""
    try:
        lunar_date = LunarDate(lunar_year, lunar_month, lunar_day)
        solar_date = lunar_date.toSolarDate()
        return {
            "lunar_date": f"{lunar_year}年{get_lunar_month_name(lunar_month)}{get_lunar_day_name(lunar_day)}",
            "solar_date": solar_date.strftime("%Y-%m-%d")
        }
    except Exception as e:
        return {"error": f"转换失败: {str(e)}"}

def get_lunar_month_name(month):
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]
    return lunar_months[month - 1] if 1 <= month <= 12 else f"{month}月"

def get_lunar_day_name(day):
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    return lunar_days[day - 1] if 1 <= day <= 30 else f"{day}日"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python simple_lunar.py --solar YYYY-MM-DD 或 --lunar YYYY MM DD")
        sys.exit(1)
    
    if sys.argv[1] == "--solar" and len(sys.argv) == 3:
        result = solar_to_lunar(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif sys.argv[1] == "--lunar" and len(sys.argv) == 5:
        result = lunar_to_solar(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print("参数错误")
        sys.exit(1)