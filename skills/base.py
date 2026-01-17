from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the skill (e.g., 'anti_gravity')"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description for the LLM to understand when to use this skill"""
        pass

    @abstractmethod
    def execute(self, data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual logic"""
        pass
