import pytest
import asyncio
from hermes.cron.scheduler import AsyncCronScheduler
from hermes.cron.tasks.daily_briefing import execute_daily_briefing
from hermes.cron.tasks.memory_compaction import execute_memory_compaction

def test_cron_scheduler():
    scheduler = AsyncCronScheduler()
    counter = 0

    async def sample_job():
        nonlocal counter
        counter += 1

    scheduler.add_job("sample_task", "Sample Task", interval_seconds=1, handler=sample_job)
    assert len(scheduler._tasks) == 1

    asyncio.run(scheduler.run_task_once("sample_task"))
    assert counter == 1
    assert scheduler._tasks["sample_task"].run_count == 1

def test_builtin_cron_jobs():
    res1 = asyncio.run(execute_daily_briefing())
    assert res1["status"] == "success"
    assert "Morning Executive Briefing" in res1["briefing"]

    res2 = asyncio.run(execute_memory_compaction())
    assert res2["status"] == "success"
