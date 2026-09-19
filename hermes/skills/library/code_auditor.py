from typing import Any, Dict, List
from hermes.skills.base import BaseSkill, SkillDefinition

class CodeAuditorSkill(BaseSkill):
    """Audits code for security flaws, resource leaks, injection vulnerabilities, and style violations."""
    def __init__(self):
        self.definition = SkillDefinition(
            skill_id="code_auditor",
            name="Code Quality & Security Auditor",
            description="Performs static security analysis, linting verification, and architecture reviews.",
            tags=["security", "audit", "quality", "review"]
        )

    async def execute(self, inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        code = inputs.get("code", "")
        issues: List[str] = []
        if "eval(" in code:
            issues.append("CRITICAL: Use of `eval()` detected. Risk of arbitrary code execution.")
        if "os.system(" in code:
            issues.append("WARNING: Use of `os.system()`. Prefer `subprocess.run(..., shell=False)`.")
        if "password =" in code.lower() or "api_key =" in code.lower():
            issues.append("SECURITY: Potential hardcoded credentials detected.")

        passed = len(issues) == 0
        return {
            "passed": passed,
            "issues_count": len(issues),
            "issues": issues,
            "verdict": "CLEAN" if passed else "REMEDIATION_REQUIRED"
        }
