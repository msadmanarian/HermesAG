import pytest
import asyncio
from hermes.tools.mcp.client import MCPClient
from hermes.tools.mcp.servers.notebooklm_mcp import NotebookLMMCPServer
from hermes.tools.mcp.servers.obsidian_mcp import ObsidianMCPServer

def test_mcp_client_registration():
    client = MCPClient("notebooklm")
    for t_def in NotebookLMMCPServer.get_definitions():
        client.register_server_tool(t_def)
    
    assert len(client.list_tools()) == 2
    res = asyncio.run(client.call_tool("notebooklm_query", {"notebook_id": "nb_1", "query": "agent architecture"}))
    assert res["status"] == "success"

def test_mcp_server_direct_calls():
    nb = NotebookLMMCPServer()
    res = asyncio.run(nb.handle_call("notebooklm_query", {"query": "test query"}))
    assert "citations" in res

    obs = ObsidianMCPServer()
    obs_res = asyncio.run(obs.handle_call("obsidian_search", {"query": "pomodoro"}))
    assert len(obs_res["matches"]) >= 1
