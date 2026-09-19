import sys
import subprocess
from typing import Any, Dict
from hermes.tools.base import BaseTool, ToolParameter

class CodeExecutionTool(BaseTool):
    name = "code_exec"
    description = "Executes Python code in an isolated subprocess sandbox and returns stdout/stderr."
    parameters = [
        ToolParameter(name="code", type="string", description="The Python source code to execute.", required=True),
        ToolParameter(name="timeout_sec", type="integer", description="Maximum allowed runtime in seconds.", required=False, default=15)
    ]

    async def execute(self, code: str, timeout_sec: int = 15) -> Dict[str, Any]:
        try:
            res = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            return {
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "success": res.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "stdout": "", "stderr": f"Execution timed out after {timeout_sec}s", "success": False}
        except Exception as e:
            return {"exit_code": -1, "stdout": "", "stderr": str(e), "success": False}
