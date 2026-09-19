from pathlib import Path
from typing import Any, Dict, List
from hermes.tools.base import BaseTool, ToolParameter

class FileOpsTool(BaseTool):
    name = "file_ops"
    description = "Read, write, list, and verify local files inside the workspace."
    parameters = [
        ToolParameter(name="action", type="string", description="Action: 'read', 'write', 'list', 'exists'", required=True),
        ToolParameter(name="path", type="string", description="File or directory path.", required=True),
        ToolParameter(name="content", type="string", description="Content to write when action is 'write'.", required=False, default="")
    ]

    async def execute(self, action: str, path: str, content: str = "") -> Dict[str, Any]:
        p = Path(path)
        if action == "read":
            if not p.exists():
                return {"error": f"File not found: {path}", "success": False}
            return {"content": p.read_text(encoding="utf-8"), "success": True}
        elif action == "write":
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return {"message": f"Wrote {len(content)} bytes to {path}", "success": True}
        elif action == "list":
            if not p.exists():
                return {"error": f"Directory not found: {path}", "success": False}
            files = [str(f.name) for f in p.iterdir()]
            return {"files": files, "success": True}
        elif action == "exists":
            return {"exists": p.exists(), "success": True}
        return {"error": f"Unknown action: {action}", "success": False}
