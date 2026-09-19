# Hardware Options & Deployment Guide

Based on Tina Huang's *Hermes Agent Fundamentals*:

### 1. Dedicated Local Machine (e.g. Mac Studio 64GB)
- Best for local open-source LLMs (Qwen 2.5 32B / Llama 3.3 70B via Ollama / llama.cpp).
- Complete data privacy and zero API costs.

### 2. Low-Cost Virtual Private Server (VPS) ($5–$6/mo)
- 24/7 background cron intelligence routines.
- Connects to Anthropic Claude or OpenAI APIs.

### 3. Docker Container Sandbox
- Runs untrusted agent-generated code safely with isolated network and storage caps.
