import os
from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx
from hermes.core.types import Message, ToolCall
from hermes.models.base import BaseModelProvider, ModelResponse, ModelStreamChunk

class AnthropicProvider(BaseModelProvider):
    """Anthropic Messages API provider supporting Claude 3.5 Sonnet & Claude 3.7."""
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"

    def _build_payload(self, messages: List[Message], system_prompt: Optional[str], tools: Optional[List[Dict[str, Any]]], max_tokens: int):
        formatted = []
        for m in messages:
            formatted.append({"role": m.role.value if m.role.value != "system" else "user", "content": m.content})
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": formatted
        }
        if system_prompt:
            payload["system"] = system_prompt
        if tools:
            payload["tools"] = tools
        return payload

    async def generate(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> ModelResponse:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = self._build_payload(messages, system_prompt, tools, max_tokens)
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{self.base_url}/messages", json=payload, headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"Anthropic API error: {resp.status_code} - {resp.text}")
            data = resp.json()
            content = data.get("content", [{}])[0].get("text", "")
            return ModelResponse(content=content, model_name=self.model)

    async def stream(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> AsyncGenerator[ModelStreamChunk, None]:
        resp = await self.generate(messages, system_prompt, tools, temperature, max_tokens)
        yield ModelStreamChunk(delta=resp.content, is_finished=True)
