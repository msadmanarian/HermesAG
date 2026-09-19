from pathlib import Path
from typing import Any, Dict, List, Optional
from hermes.core.types import Message
from hermes.memory.tier1_core import Tier1CoreMemory
from hermes.memory.tier2_sqlite import Tier2SessionMemory
from hermes.memory.tier3_honcho import Tier3CognitiveTracker
from hermes.memory.tier4_obsidian import Tier4ObsidianVault
from hermes.memory.tier4_prd import ObsidianPRDManager

class UnifiedMemoryManager:
    """
    Orchestrates the complete 4-Tier Memory Architecture:
    - Tier 1: Core Files (memory.md, user.md, soul.md)
    - Tier 2: SQLite Episodic Session DB with FTS5 lexical indexing
    - Tier 3: Honcho-style Cognitive Pattern Profiler
    - Tier 4: Obsidian Second Brain Vault & PRD Manager
    """
    def __init__(
        self,
        tier1_dir: str | Path = "data/tier1_core",
        tier2_db: str | Path = "data/tier2_sessions.db",
        tier3_profile: str | Path = "data/tier3_profile.json",
        tier4_vault: str | Path = "data/obsidian_vault"
    ):
        self.tier1 = Tier1CoreMemory(tier1_dir)
        self.tier2 = Tier2SessionMemory(tier2_db)
        self.tier3 = Tier3CognitiveTracker(tier3_profile)
        self.tier4 = Tier4ObsidianVault(tier4_vault)
        self.prd_manager = ObsidianPRDManager(self.tier4)

    def record_interaction(self, session_id: str, user_msg: Message, assistant_msg: Message):
        # Tier 2: Log to episodic database
        self.tier2.log_message(session_id, user_msg)
        self.tier2.log_message(session_id, assistant_msg)
        
        # Tier 3: Observe user cognitive patterns
        self.tier3.observe_message(user_msg)

    def build_augmented_context(self, session_id: str, current_query: str) -> str:
        """Assembles multi-tier cognitive context to inject into LLM prompts."""
        t1_context = self.tier1.render_system_prompt_context()
        t3_context = self.tier3.render_tier3_context()
        
        # Tier 2 relevant recall
        search_results = self.tier2.search(current_query, limit=3)
        t2_snippets = "\n".join(f"- [{r['role']} in {r['session_id']}]: {r['snippet']}" for r in search_results)
        t2_context = f"=== TIER 2 EPISODIC RECALL ===\n{t2_snippets if t2_snippets else '- No prior matching episodes.'}\n==============================="
        
        return f"{t1_context}\n\n{t3_context}\n\n{t2_context}"
