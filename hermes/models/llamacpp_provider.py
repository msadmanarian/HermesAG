from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx
from hermes.core.types import Message
from hermes.models.base import BaseModelProvider, ModelResponse, ModelStreamChunk

class LlamaCppProvider(BaseModelProvider):
    """
    High-performance, low-level local model provider connecting directly to a llama.cpp server.
    Optimized for quantized GGUF models on dedicated hardware.
    """
    def __init__(self, server_url: str = "http://localhost:8080", model: str = "local-gguf"):
        self.server_url = server_url.rstrip("/")
        self.model = model

    async def generate(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> ModelResponse:
        prompt = ""
        if system_prompt:
            prompt += f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        for m in messages:
            prompt += f"<|im_start|>{m.role.value}\n{m.content}<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"

        payload = {"prompt": prompt, "temperature": temperature, "n_predict": max_tokens}
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{self.server_url}/completion", json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"llama.cpp error: {resp.status_code} - {resp.text}")
            data = resp.json()
            content = data.get("content", "")
            return ModelResponse(content=content, model_name=self.model)

    async def stream(self, messages: List[Message], system_prompt: Optional[str] = None, tools: Optional[List[Dict[str, Any]]] = None, temperature: float = 0.7, max_tokens: int = 4096) -> AsyncGenerator[ModelStreamChunk, None]:
        resp = await self.generate(messages, system_prompt, tools, temperature, max_tokens)
        yield ModelStreamChunk(delta=resp.content, is_finished=True)
