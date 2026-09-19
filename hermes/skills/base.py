from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class SkillStep(BaseModel):
    step_id: str
    name: str
    description: str
    action_type: str = "prompt" # prompt, tool_call, validation

class SkillDefinition(BaseModel):
    skill_id: str
    name: str
    description: str
    version: str = "1.0.0"
    steps: List[SkillStep] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

class BaseSkill(ABC):
    definition: SkillDefinition

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        pass

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}

    def register(self, skill: BaseSkill):
        self._skills[skill.definition.skill_id] = skill

    def get(self, skill_id: str) -> Optional[BaseSkill]:
        return self._skills.get(skill_id)

    def list_skills(self) -> List[SkillDefinition]:
        return [s.definition for s in self._skills.values()]
