from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SoulIdentity(BaseModel):
    name: str = "Hermes"
    persona: str = "Autonomous Executive Agent and Technical Copilot"
    voice: str = "Concise, highly capable, proactive, and rigorously truthful"
    core_directives: List[str] = Field(default_factory=lambda: [
        "Prioritize user intent and mission success above verbose explanations.",
        "Maintain deep continuous memory across conversations and sessions.",
        "Proactively inspect code, execute tests, and verify before claiming success.",
        "Reflect on errors and update internal operational strategies."
    ])

class UserProfile(BaseModel):
    user_id: str = "primary_user"
    name: str = "Operator"
    role: str = "Engineer & Founder"
    preferences: Dict[str, Any] = Field(default_factory=lambda: {
        "communication_style": "direct_and_dense",
        "primary_stack": ["Python", "TypeScript", "FastAPI", "React", "Docker"],
        "operating_system": "windows_and_linux",
        "timezone": "UTC+6"
    })
    long_term_goals: List[str] = Field(default_factory=lambda: [
        "Build reliable autonomous multi-agent pipelines.",
        "Integrate 4-tier persistent memory with Obsidian Second Brain.",
        "Execute 24/7 background cron intelligence routines."
    ])

class SystemMemory(BaseModel):
    facts: List[str] = Field(default_factory=list)
    project_states: Dict[str, str] = Field(default_factory=dict)
    known_limitations: List[str] = Field(default_factory=list)
