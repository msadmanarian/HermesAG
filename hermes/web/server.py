import os
from pathlib import Path
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from hermes.hardware.runtime import HardwareRuntimeDetector
from hermes.memory.manager import UnifiedMemoryManager
from hermes.core.types import Message, MessageRole
from hermes.models.mock_provider import MockModelProvider

app = FastAPI(title="HermesAG Dashboard Server", version="0.1.0")

STATIC_DIR = Path(__file__).resolve().parent / "static"
memory_mgr = UnifiedMemoryManager()
model_provider = MockModelProvider()

@app.get("/api/status")
async def get_status():
    hw = HardwareRuntimeDetector.detect()
    return {
        "status": "online",
        "agent": "Hermes",
        "hardware": hw.model_dump(),
        "memory_tiers": {
            "tier1_facts": len(memory_mgr.tier1.system_memory.facts),
            "tier3_patterns": len(memory_mgr.tier3.profile.patterns),
            "tier4_notes": len(memory_mgr.tier4.list_notes())
        }
    }

@app.get("/api/memory/tier1")
async def get_tier1():
    return {
        "soul": memory_mgr.tier1.soul.model_dump(),
        "user": memory_mgr.tier1.user.model_dump(),
        "facts": memory_mgr.tier1.system_memory.facts
    }

@app.get("/api/memory/tier3")
async def get_tier3():
    return {
        "patterns": memory_mgr.tier3.profile.patterns,
        "interests": memory_mgr.tier3.get_top_interests(10)
    }

@app.get("/api/memory/tier4")
async def get_tier4():
    notes = memory_mgr.tier4.list_notes()
    return {"notes": notes}

@app.post("/api/chat")
async def chat_endpoint(payload: Dict[str, Any]):
    user_text = payload.get("message", "").strip()
    if not user_text:
        raise HTTPException(status_code=400, detail="Empty message")
    
    session_id = payload.get("session_id", "web_default")
    user_msg = Message(role=MessageRole.USER, content=user_text)
    
    augmented_context = memory_mgr.build_augmented_context(session_id, user_text)
    resp = await model_provider.generate([user_msg], system_prompt=augmented_context)
    
    assistant_msg = Message(role=MessageRole.ASSISTANT, content=resp.content)
    memory_mgr.record_interaction(session_id, user_msg, assistant_msg)
    
    return {
        "reply": resp.content,
        "model": resp.model_name
    }

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def serve_index():
        index_file = STATIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return HTMLResponse("<h2>HermesAG Dashboard Ready</h2>")
