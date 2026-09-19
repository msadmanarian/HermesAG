import asyncio
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

CronHandler = Callable[[], Coroutine[Any, Any, None]]

class CronTask(BaseModel):
    task_id: str
    name: str
    interval_seconds: int
    last_run: Optional[datetime] = None
    run_count: int = 0
    is_enabled: bool = True

class AsyncCronScheduler:
    """
    Background scheduled task runner for HermesAG 24/7 continuous operations.
    Executes periodic routines such as daily briefings, memory compaction, and obsidian vault sync.
    """
    def __init__(self):
        self._tasks: Dict[str, CronTask] = {}
        self._handlers: Dict[str, CronHandler] = {}
        self._running = False
        self._loop_task: Optional[asyncio.Task] = None

    def add_job(self, task_id: str, name: str, interval_seconds: int, handler: CronHandler):
        self._tasks[task_id] = CronTask(task_id=task_id, name=name, interval_seconds=interval_seconds)
        self._handlers[task_id] = handler

    async def run_task_once(self, task_id: str):
        if task_id in self._handlers and self._tasks[task_id].is_enabled:
            handler = self._handlers[task_id]
            task = self._tasks[task_id]
            try:
                await handler()
                task.last_run = datetime.now(timezone.utc)
                task.run_count += 1
            except Exception as e:
                print(f"[Cron Error] Task {task_id} failed: {e}")

    async def start(self):
        self._running = True
        self._loop_task = asyncio.create_task(self._main_loop())

    async def stop(self):
        self._running = False
        if self._loop_task:
            self._loop_task.cancel()
            try:
                await self._loop_task
            except asyncio.CancelledError:
                pass

    async def _main_loop(self):
        while self._running:
            now = datetime.now(timezone.utc)
            for t_id, task in self._tasks.items():
                if not task.is_enabled:
                    continue
                should_run = False
                if task.last_run is None:
                    should_run = True
                else:
                    elapsed = (now - task.last_run).total_seconds()
                    if elapsed >= task.interval_seconds:
                        should_run = True
                if should_run:
                    await self.run_task_once(t_id)
            await asyncio.sleep(1)
