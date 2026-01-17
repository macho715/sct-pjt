from typing import Dict, Type
from .base import BaseSkill
from .anti_gravity import AntiGravitySkill
from .anti_gravity_v2 import AdvancedAntiGravitySkill
from .visualization import GanttChartSkill

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        # Register default skills
        self.register(AntiGravitySkill())
        self.register(AdvancedAntiGravitySkill())
        self.register(GanttChartSkill())

    def register(self, skill: BaseSkill):
        self._skills[skill.name] = skill
        print(f"Skill Registered: [{skill.name}]")

    def get_skill(self, name: str) -> BaseSkill:
        return self._skills.get(name)

    def list_skills(self):
        return {name: skill.description for name, skill in self._skills.items()}

# Global Instance
registry = SkillRegistry()
