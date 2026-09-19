import asyncio
from typing import Any, Callable, Coroutine, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class Event(BaseModel):
    name: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

EventHandler = Callable[[Event], Coroutine[Any, Any, None]]

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler):
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    async def publish(self, event_name: str, payload: Dict[str, Any] | None = None):
        event = Event(name=event_name, payload=payload or {})
        handlers = self._subscribers.get(event_name, [])
        if handlers:
            await asyncio.gather(*(h(event) for h in handlers), return_exceptions=True)

    def unsubscribe(self, event_name: str, handler: EventHandler):
        if event_name in self._subscribers and handler in self._subscribers[event_name]:
            self._subscribers[event_name].remove(handler)
