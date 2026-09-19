from typing import Any, AsyncGenerator, Dict, List, Optional
from hermes.core.types import Message, ToolCall
from hermes.models.base import BaseModelProvider, ModelResponse, ModelStreamChunk

class MockModelProvider(BaseModelProvider):
    """
    Deterministic offline model provider for fast testing, automated benchmarks, and zero-cost local execution.
    """
    def __init__(self, default_reply: str = "I am Hermes, your technical agent."):
        self.default_reply = default_reply
        self.canned_responses: Dict[str, ModelResponse] = {}

    def register_response(self, keyword: str, response: ModelResponse):
        self.canned_responses[keyword.lower()] = response

    async def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> ModelResponse:
        last_msg = messages[-1].content.lower() if messages else ""
        for k, resp in self.canned_responses.items():
            if k in last_msg:
                return resp
        return ModelResponse(
            content=self.default_reply,
            model_name="hermes-mock-v1",
            usage={"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70}
        )

    async def stream(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> AsyncGenerator[ModelStreamChunk, None]:
        response = await self.generate(messages, system_prompt, tools, temperature, max_tokens)
        words = response.content.split()
        for i, word in enumerate(words):
            yield ModelStreamChunk(
                delta=word + (" " if i < len(words) - 1 else ""),
                is_finished=(i == len(words) - 1)
            )
