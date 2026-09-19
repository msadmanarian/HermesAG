import asyncio
from hermes.core.types import Message, MessageRole, ToolCall, AgentState
from hermes.core.events import EventBus
from hermes.core.context import ExecutionContext

def test_message_and_tool_call():
    tc = ToolCall(id="call_1", name="search", arguments={"query": "Hermes AI"})
    msg = Message(role=MessageRole.ASSISTANT, content="Searching...", tool_calls=[tc])
    assert msg.role == MessageRole.ASSISTANT
    assert len(msg.tool_calls) == 1
    assert msg.tool_calls[0].name == "search"

def test_event_bus():
    bus = EventBus()
    received = []

    async def on_state_change(event):
        received.append(event.payload.get("new_state"))

    bus.subscribe("state_changed", on_state_change)
    asyncio.run(bus.publish("state_changed", {"new_state": "acting"}))
    assert received == ["acting"]

def test_execution_context():
    ctx = ExecutionContext()
    assert ctx.current_state == AgentState.IDLE
    ctx.transition_to(AgentState.THINKING)
    assert ctx.current_state == AgentState.THINKING
    assert ctx.step_count == 1
    ctx.set_var("goal", "build pomodoro")
    assert ctx.get_var("goal") == "build pomodoro"
