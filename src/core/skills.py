"""
Qji Max Skill System - Plugin-based extensible functionality
"""
import asyncio
import importlib
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

class BaseSkill(ABC):
    """Base class for all Qji Max skills"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enabled = True
        
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill with given parameters"""
        pass
    
    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """Check if this skill can handle the given query"""
        pass

class SkillManager:
    """Manages all available skills and their execution"""
    
    def __init__(self):
        self.skills: Dict[str, BaseSkill] = {}
        self.skill_dir = Path(__file__).parent.parent / "skills"
        self._load_skills()
        
    def _load_skills(self):
        """Load all skills from the skills directory"""
        if not self.skill_dir.exists():
            self.skill_dir.mkdir(exist_ok=True)
            # Create example skill
            self._create_example_skill()
            return
            
        # Load built-in skills
        self._load_builtin_skills()
        
        # Load custom skills
        for skill_file in self.skill_dir.glob("*.py"):
            if skill_file.name != "__init__.py":
                try:
                    module_name = f"qianji.skills.{skill_file.stem}"
                    spec = importlib.util.spec_from_file_location(module_name, skill_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find skill classes
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, BaseSkill) and 
                            attr != BaseSkill):
                            skill_instance = attr()
                            self.skills[skill_instance.name] = skill_instance
                            print(f"✅ Loaded skill: {skill_instance.name}")
                            
                except Exception as e:
                    print(f"❌ Failed to load skill {skill_file.name}: {e}")
    
    def _load_builtin_skills(self):
        """Load built-in skills"""
        from .web_search import WebSearchSkill
        web_search_skill = WebSearchSkill()
        self.skills[web_search_skill.name] = web_search_skill
        print(f"✅ Loaded built-in skill: {web_search_skill.name}")
    
    def _create_example_skill(self):
        """Create an example skill file"""
        example_skill = '''
"""
Example Skill for Qji Max
"""
from qianji.core.skills import BaseSkill
import asyncio

class ExampleSkill(BaseSkill):
    def __init__(self):
        super().__init__("example", "Example skill that demonstrates the skill system")
    
    async def execute(self, **kwargs):
        query = kwargs.get('query', '')
        return {
            'success': True,
            'result': f"Example skill processed: {query}",
            'skill_used': self.name
        }
    
    def can_handle(self, query: str) -> bool:
        return 'example' in query.lower()
'''
        with open(self.skill_dir / "example_skill.py", "w") as f:
            f.write(example_skill)
    
    async def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific skill"""
        if skill_name not in self.skills:
            return {'success': False, 'error': f'Skill {skill_name} not found'}
        
        skill = self.skills[skill_name]
        if not skill.enabled:
            return {'success': False, 'error': f'Skill {skill_name} is disabled'}
            
        try:
            result = await skill.execute(**kwargs)
            result['skill_used'] = skill_name
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def find_appropriate_skill(self, query: str) -> Optional[str]:
        """Find the most appropriate skill for a given query"""
        for skill_name, skill in self.skills.items():
            if skill.enabled and skill.can_handle(query):
                return skill_name
        return None
    
    async def execute_all_relevant_skills(self, query: str, max_concurrent: int = 3) -> List[Dict[str, Any]]:
        """Execute all relevant skills in parallel"""
        relevant_skills = []
        for skill_name, skill in self.skills.items():
            if skill.enabled and skill.can_handle(query):
                relevant_skills.append(skill_name)
        
        if not relevant_skills:
            return [{'success': False, 'error': 'No relevant skills found'}]
        
        # Execute skills in parallel with concurrency limit
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def execute_with_semaphore(skill_name):
            async with semaphore:
                return await self.execute_skill(skill_name, query=query)
        
        tasks = [execute_with_semaphore(skill_name) for skill_name in relevant_skills]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append({
                    'success': False, 
                    'error': str(result),
                    'skill_used': relevant_skills[i]
                })
            else:
                final_results.append(result)
                
        return final_results

# Global skill manager instance
skill_manager = SkillManager()