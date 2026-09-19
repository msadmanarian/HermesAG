import pytest
import asyncio
from hermes.skills.base import SkillRegistry
from hermes.skills.library.business_evaluator import BusinessIdeaEvaluatorSkill
from hermes.skills.library.prd_generator import PRDGeneratorSkill
from hermes.skills.library.pomodoro_builder import PomodoroBuilderSkill
from hermes.skills.library.code_auditor import CodeAuditorSkill

def test_skills_execution():
    registry = SkillRegistry()
    registry.register(BusinessIdeaEvaluatorSkill())
    registry.register(PRDGeneratorSkill())
    registry.register(PomodoroBuilderSkill())
    registry.register(CodeAuditorSkill())

    assert len(registry.list_skills()) == 4

    # 1. Business Evaluator
    biz_skill = registry.get("business_idea_evaluator")
    biz_res = asyncio.run(biz_skill.execute({"idea": "AI Meeting Assistant"}))
    assert biz_res["score"] > 8.0
    assert "PROCEED" in biz_res["verdict"]

    # 2. PRD Generator
    prd_skill = registry.get("prd_generator")
    prd_res = asyncio.run(prd_skill.execute({"feature_name": "Obsidian Sync"}))
    assert "Obsidian Sync" in prd_res["prd_markdown"]

    # 3. Pomodoro Builder
    pomo_skill = registry.get("pomodoro_builder")
    pomo_res = asyncio.run(pomo_skill.execute({}))
    assert "FloatingPomodoroApp" in pomo_res["code"]

    # 4. Code Auditor
    audit_skill = registry.get("code_auditor")
    clean_res = asyncio.run(audit_skill.execute({"code": "def hello(): return 'world'"}))
    assert clean_res["passed"] is True

    vuln_res = asyncio.run(audit_skill.execute({"code": "eval(user_input)"}))
    assert vuln_res["passed"] is False
    assert len(vuln_res["issues"]) == 1
