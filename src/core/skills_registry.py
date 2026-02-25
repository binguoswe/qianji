"""
Skills Registry for Qji Max AI
Central registry for all available skills and their capabilities
"""

from typing import Dict, List, Any
from .skills import SkillBase

# Built-in skills registry
BUILTIN_SKILLS = {
    "web_search": {
        "name": "Web Search",
        "description": "Search the web for current information using Brave Search API",
        "module": "src.core.web_search",
        "class": "WebSearchSkill",
        "enabled": True,
        "requires_api_key": True
    },
    "bazi_analysis": {
        "name": "Bazi Analysis", 
        "description": "Professional八字命理分析 with deep classical knowledge",
        "module": "src.core.bazi_engine",
        "class": "BaziEngine",
        "enabled": True,
        "requires_api_key": False
    },
    "feng_shui": {
        "name": "Feng Shui Analysis",
        "description": "风水罗盘分析和环境布局建议",
        "module": "src.core.feng_shui_engine", 
        "class": "FengShuiEngine",
        "enabled": False,  # Placeholder for future implementation
        "requires_api_key": False
    }
}

def get_available_skills() -> Dict[str, Dict[str, Any]]:
    """Get all available skills with their metadata"""
    return BUILTIN_SKILLS.copy()

def is_skill_enabled(skill_name: str) -> bool:
    """Check if a skill is enabled"""
    return BUILTIN_SKILLS.get(skill_name, {}).get("enabled", False)

def get_skill_class(skill_name: str):
    """Get the skill class for instantiation"""
    if not is_skill_enabled(skill_name):
        return None
    
    skill_info = BUILTIN_SKILLS[skill_name]
    module_name = skill_info["module"]
    class_name = skill_info["class"]
    
    # Dynamic import
    import importlib
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

# Initialize skill instances cache
SKILL_INSTANCES = {}

def get_skill_instance(skill_name: str) -> SkillBase:
    """Get or create a skill instance"""
    if skill_name not in SKILL_INSTANCES:
        skill_class = get_skill_class(skill_name)
        if skill_class:
            SKILL_INSTANCES[skill_name] = skill_class()
        else:
            return None
    return SKILL_INSTANCES[skill_name]