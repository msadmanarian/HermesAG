from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional
from pydantic import BaseModel, Field
from hermes.core.types import Message, ToolCall

class ModelResponse(BaseModel):
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    finish_reason: str = "stop"
    usage: Dict[str, int] = Field(default_factory=dict)
    model_name: str = "unknown"

class ModelStreamChunk(BaseModel):
    delta: str = ""
    tool_call_chunk: Optional[ToolCall] = None
    is_finished: bool = False

class BaseModelProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> ModelResponse:
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> AsyncGenerator[ModelStreamChunk, None]:
        pass
