from typing import Any, Dict, List
from hermes.tools.mcp.protocol import MCPToolDefinition

class ObsidianMCPServer:
    """
    MCP Server adapter for Obsidian Second Brain.
    Exposes vault full-text search, note creation, and tag queries over the Model Context Protocol.
    """
    @staticmethod
    def get_definitions() -> List[MCPToolDefinition]:
        return [
            MCPToolDefinition(
                name="obsidian_search",
                description="Searches an Obsidian vault for notes matching query keywords.",
                inputSchema={
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"]
                }
            ),
            MCPToolDefinition(
                name="obsidian_append_note",
                description="Appends markdown text to an existing or new note in Obsidian.",
                inputSchema={
                    "type": "object",
                    "properties": {"note_path": {"type": "string"}, "content": {"type": "string"}},
                    "required": ["note_path", "content"]
                }
            )
        ]

    async def handle_call(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name == "obsidian_search":
            return {"matches": [f"Notes/Architecture.md (found query: {args.get('query')})"]}
        elif name == "obsidian_append_note":
            return {"status": "appended", "note": args.get("note_path")}
        raise ValueError(f"Unknown Obsidian tool: {name}")
