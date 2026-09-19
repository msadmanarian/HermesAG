import pytest
import asyncio
from hermes.tools.base import ToolRegistry
from hermes.tools.code_exec import CodeExecutionTool
from hermes.tools.file_ops import FileOpsTool
from hermes.tools.web_search import WebSearchTool

def test_tool_registry():
    registry = ToolRegistry()
    code_tool = CodeExecutionTool()
    registry.register(code_tool)

    assert registry.get("code_exec") is not None
    schemas = registry.list_schemas()
    assert len(schemas) == 1
    assert schemas[0]["function"]["name"] == "code_exec"

def test_code_execution():
    tool = CodeExecutionTool()
    res = asyncio.run(tool.execute(code="print(21 + 21)"))
    assert res["success"] is True
    assert "42" in res["stdout"]

def test_file_ops(tmp_path):
    tool = FileOpsTool()
    file_path = str(tmp_path / "test.txt")
    write_res = asyncio.run(tool.execute(action="write", path=file_path, content="Hermes Tool Test"))
    assert write_res["success"] is True

    read_res = asyncio.run(tool.execute(action="read", path=file_path))
    assert read_res["success"] is True
    assert read_res["content"] == "Hermes Tool Test"
