from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx
from hermes.core.types import Message
from hermes.models.base import BaseModelProvider, ModelResponse, ModelStreamChunk

class OllamaProvider(BaseModelProvider):
    """
    Local open-source model provider via Ollama.
    Supports Qwen 2.5, Llama 3.3, and DeepSeek running locally on Mac Studio or local GPUs.
    """
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:7b"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> ModelResponse:
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        for m in messages:
            msgs.append({"role": m.role.value, "content": m.content})

        payload = {"model": self.model, "messages": msgs, "stream": False, "options": {"temperature": temperature}}
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Ollama error: {resp.status_code} - {resp.text}")
            data = resp.json()
            content = data.get("message", {}).get("content", "")
            return ModelResponse(content=content, model_name=self.model)

    async def stream(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> AsyncGenerator[ModelStreamChunk, None]:
        resp = await self.generate(messages, system_prompt, tools, temperature, max_tokens)
        yield ModelStreamChunk(delta=resp.content, is_finished=True)
