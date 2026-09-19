import os
from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx
from hermes.core.types import Message, ToolCall
from hermes.models.base import BaseModelProvider, ModelResponse, ModelStreamChunk

class OpenAIProvider(BaseModelProvider):
    """OpenAI / OpenRouter Chat Completions standard API provider."""
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> ModelResponse:
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        for m in messages:
            msgs.append({"role": m.role.value, "content": m.content})

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": msgs, "temperature": temperature, "max_tokens": max_tokens}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"OpenAI API error: {resp.status_code} - {resp.text}")
            data = resp.json()
            choice = data["choices"][0]
            return ModelResponse(content=choice["message"].get("content", ""), model_name=self.model)

    async def stream(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> AsyncGenerator[ModelStreamChunk, None]:
        resp = await self.generate(messages, system_prompt, tools, temperature, max_tokens)
        yield ModelStreamChunk(delta=resp.content, is_finished=True)
