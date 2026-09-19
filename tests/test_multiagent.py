import pytest
import asyncio
from hermes.multiagent.coordinator import MultiAgentCoordinator
from hermes.multiagent.team import get_standard_team_roles

def test_multiagent_pipeline():
    coord = MultiAgentCoordinator()
    for role in get_standard_team_roles():
        coord.register_role(role)
    
    pipeline = ["architect", "coder", "critic", "executive"]
    res = asyncio.run(coord.execute_task_pipeline("Build a Floating Pomodoro App with Obsidian Sync", pipeline))
    
    assert res["status"] == "completed"
    assert len(res["stages"]) == 4
    assert "architect" in res["stages"]
    assert "coder" in res["stages"]
    assert "critic" in res["stages"]
    assert "executive" in res["stages"]
