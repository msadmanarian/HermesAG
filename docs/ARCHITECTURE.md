# HermesAG System Architecture

HermesAG is an open-source, multi-tier cognitive agent architecture engineered for 24/7 autonomous operations across local machines, VPS cloud nodes, and isolated Docker sandboxes.

```mermaid
graph TD
    User([User / Operator]) --> Gateways[Gateways: CLI / Discord / Telegram / Web]
    Gateways --> Core[Hermes Core Agent Loop]
    
    subgraph 4-Tier Memory Architecture
        Core --> T1[Tier 1: Core Files memory.md, user.md, soul.md]
        Core --> T2[Tier 2: Episodic SQLite DB with FTS5]
        Core --> T3[Tier 3: Honcho Cognitive Pattern Tracker]
        Core --> T4[Tier 4: Obsidian Second Brain Vault & PRDs]
    end

    subgraph Tool & MCP Ecosystem
        Core --> Tools[Web Search, Code Exec, Browser, FileOps]
        Core --> MCP[Model Context Protocol Client]
        MCP --> NotebookLM[NotebookLM MCP Server]
        MCP --> ObsidianMCP[Obsidian MCP Server]
    end

    subgraph Pluggable Models
        Core --> Models[Claude 3.5 Sonnet / OpenAI / Ollama Qwen / llama.cpp]
    end
```
