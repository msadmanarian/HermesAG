from hermes.multiagent.coordinator import AgentRole

def get_standard_team_roles() -> list[AgentRole]:
    return [
        AgentRole(
            role_id="architect",
            name="System Architect",
            system_prompt="You design clean, modular software specifications and verify system scalability.",
            capabilities=["spec_design", "database_modeling", "api_contracts"]
        ),
        AgentRole(
            role_id="coder",
            name="Principal Engineer",
            system_prompt="You write robust, readable, idiomatic production code with clean error handling.",
            capabilities=["code_generation", "refactoring", "dependency_management"]
        ),
        AgentRole(
            role_id="critic",
            name="Security & QA Critic",
            system_prompt="You rigorously audit code for edge cases, performance bottlenecks, and security flaws.",
            capabilities=["vulnerability_audit", "test_synthesis", "performance_profiling"]
        ),
        AgentRole(
            role_id="executive",
            name="Product Manager & Executive",
            system_prompt="You synthesize team outputs into user-facing deliverables and ensure alignment with PRDs.",
            capabilities=["prd_alignment", "user_acceptance", "executive_summary"]
        )
    ]
