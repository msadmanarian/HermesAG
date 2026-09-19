import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class CognitivePattern(BaseModel):
    pattern_id: str
    category: str # "preference", "communication", "work_rhythm", "tool_bias"
    description: str
    confidence: float = 0.5 # 0.0 to 1.0
    evidence_count: int = 1
    last_observed: datetime = Field(default_factory=utc_now)

class UserCognitiveProfile(BaseModel):
    user_id: str = "primary_user"
    interest_keywords: Dict[str, int] = Field(default_factory=dict)
    patterns: Dict[str, CognitivePattern] = Field(default_factory=dict)
    implicit_preferences: Dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=utc_now)
