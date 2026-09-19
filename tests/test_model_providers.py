import pytest
import asyncio
from hermes.core.types import Message, MessageRole, ToolCall
from hermes.models.mock_provider import MockModelProvider
from hermes.models.base import ModelResponse
from hermes.models.anthropic_provider import AnthropicProvider
from hermes.models.openai_provider import OpenAIProvider
from hermes.models.ollama_provider import OllamaProvider
from hermes.models.llamacpp_provider import LlamaCppProvider

def test_mock_provider():
    mock = MockModelProvider(default_reply="Default reply")
    custom = ModelResponse(content="Custom Pomodoro reply", model_name="test-model")
    mock.register_response("pomodoro", custom)

    res1 = asyncio.run(mock.generate([Message(role=MessageRole.USER, content="Hello")]))
    assert res1.content == "Default reply"

    res2 = asyncio.run(mock.generate([Message(role=MessageRole.USER, content="Can we build a pomodoro?")]))
    assert res2.content == "Custom Pomodoro reply"

def test_provider_initializations():
    anthropic = AnthropicProvider(api_key="test-key")
    assert anthropic.model == "claude-3-5-sonnet-20241022"

    openai = OpenAIProvider(api_key="test-key")
    assert openai.model == "gpt-4o"

    ollama = OllamaProvider(model="qwen2.5:7b")
    assert ollama.model == "qwen2.5:7b"

    llamacpp = LlamaCppProvider(server_url="http://localhost:8080")
    assert llamacpp.server_url == "http://localhost:8080"
