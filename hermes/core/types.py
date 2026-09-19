from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class ToolResult(BaseModel):
    tool_call_id: str
    name: str
    output: Any
    is_error: bool = False

class Message(BaseModel):
    role: MessageRole
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_results: Optional[List[ToolResult]] = None
    timestamp: datetime = Field(default_factory=utc_now)

class AgentState(str, Enum):
    IDLE = "idle"
    PERCEIVING = "perceiving"
    THINKING = "thinking"
    ACTING = "acting"
    REFLECTING = "reflecting"
    ERROR = "error"

class SessionMetadata(BaseModel):
    session_id: str
    title: str = "Untitled Session"
    created_at: datetime = Field(default_factory=utc_now)
    tags: List[str] = Field(default_factory=list)
    user_id: str = "default_user"
