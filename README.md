# HermesAG: Autonomous Agentic Generation & 4-Tier Cognitive Framework

[![CI](https://img.shields.io/badge/CI-Passing-brightgreen?style=flat-square&logo=githubactions&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?style=flat-square&logo=python&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Memory Architecture](https://img.shields.io/badge/Memory-4--Tier%20Cognitive-blueviolet?style=flat-square)](#4-tier-memory-architecture)
[![Obsidian](https://img.shields.io/badge/Sync-Obsidian%20Second%20Brain-purple?style=flat-square&logo=obsidian)](#)

A comprehensive, production-grade implementation of the **Hermes Agent** framework as detailed in Tina Huang's tutorial *"Hermes Agent Fundamentals In 29 Minutes"*.

---

## 🌟 Core Innovations & Video Highlights

1. **Hardware Options & 24/7 Operations**:
   - High-RAM Local Workstations (Mac Studio 64GB) for local Qwen/Llama models.
   - Low-cost cloud VPS ($5–$6/mo) for 24/7 background daemons.
   - Docker Container Sandboxing for safe code execution.
2. **4-Tier Hierarchical Memory Architecture**:
   - **Tier 1 (Core Files):** `memory.md`, `user.md`, and `soul.md` for permanent agent persona.
   - **Tier 2 (Session Search):** SQLite database with **FTS5 full-text indexing** for instant recall.
   - **Tier 3 (Cognitive Profiler):** Honcho-style implicit pattern and interest tracking.
   - **Tier 4 (Second Brain Integration):** Seamless bidirectional sync with **Obsidian vaults**.
3. **Pluggable Multi-Model Support**:
   - Cloud APIs: Anthropic Claude 3.5/3.7 Sonnet, OpenAI GPT-4o.
   - Local Open-Source Models: Ollama (Qwen 2.5) and direct `llama.cpp` GGUF runner.
4. **Tools, MCP & Skills Ecosystem**:
   - Built-in tools: DuckDuckGo search, headless browser, sandboxed Python code execution.
   - Model Context Protocol (MCP) clients and servers for NotebookLM and Obsidian.
   - Actionable Skills: Tina Huang's Business Idea Evaluator, PRD Generator, Floating Pomodoro App Synthesizer.
5. **Multi-Agent Orchestration & Gateways**:
   - Specialized team pipelines: Architect, Coder, Critic, Executive.
   - Interfaces: Interactive CLI, Discord bot, Telegram bot, and Web Dashboard.

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/msadmanarian/HermesAG.git
cd HermesAG

# Install with pip or uv
uv venv
uv pip install -e ".[dev]"
```

### 2. Launch Interactive CLI
```bash
python -m hermes.gateways.cli
```

### 3. Launch Web Dashboard
```bash
uvicorn hermes.web.server:app --reload --port 8000
```
Open `http://localhost:8000` to inspect the 4-tier memory visualizer and chat console.

### 4. Run Automated Test Suite
```bash
pytest -v tests/
```

---

## 📁 Repository Structure

```text
HermesAG/
├── hermes/
│   ├── core/              # Types, EventBus, ExecutionContext
│   ├── memory/            # 4-Tier Memory Architecture (Core, SQLite FTS5, Honcho, Obsidian)
│   ├── models/            # Anthropic, OpenAI, Ollama, llama.cpp, Mock
│   ├── tools/             # Web Search, Browser, Code Exec, MCP Protocol
│   ├── skills/            # Business Evaluator, PRD Generator, Pomodoro Builder
│   ├── cron/              # 24/7 Background Scheduler & Daily Briefings
│   ├── hardware/          # Hardware Detector, Docker Isolator, VPS Supervisor
│   ├── multiagent/        # Multi-Agent Pipeline & Specialized Team Roles
│   ├── gateways/          # CLI, Discord Bot, Telegram Bot
│   └── web/               # FastAPI Backend & Cyber Dashboard UI
├── tests/                 # Automated Unit & Integration Tests
├── examples/              # Floating Pomodoro App, Multi-Agent PRD Demos
├── docs/                  # Architecture, 4-Tier Memory, Hardware Guides
├── pyproject.toml         # Packaging Specification
└── README.md              # Documentation
```

---

## 📜 License
Released under the [MIT License](LICENSE).
