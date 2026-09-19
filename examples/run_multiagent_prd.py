import asyncio
from hermes.multiagent.coordinator import MultiAgentCoordinator
from hermes.multiagent.team import get_standard_team_roles

async def main():
    coord = MultiAgentCoordinator()
    for r in get_standard_team_roles():
        coord.register_role(r)
    
    print("=== Launching Multi-Agent Team ===")
    res = await coord.execute_task_pipeline(
        prompt="Design and implement a multi-agent Discord research assistant.",
        pipeline_roles=["architect", "coder", "critic", "executive"]
    )
    for role, output in res["stages"].items():
        print(f"\n[{role.upper()}]:\n{output}")

if __name__ == "__main__":
    asyncio.run(main())
