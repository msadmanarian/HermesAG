import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from hermes.core.types import AgentState, Message

class ExecutionContext(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current_state: AgentState = AgentState.IDLE
    history: List[Message] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    step_count: int = 0

    def transition_to(self, new_state: AgentState):
        self.current_state = new_state
        self.step_count += 1

    def append_message(self, message: Message):
        self.history.append(message)

    def set_var(self, key: str, value: Any):
        self.variables[key] = value

    def get_var(self, key: str, default: Any = None) -> Any:
        return self.variables.get(key, default)
