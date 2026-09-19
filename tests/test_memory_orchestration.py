import tempfile
import shutil
from pathlib import Path
from hermes.core.types import Message, MessageRole
from hermes.memory.manager import UnifiedMemoryManager

def test_unified_4tier_memory():
    temp_dir = tempfile.mkdtemp()
    try:
        t1 = Path(temp_dir) / "t1"
        t2 = Path(temp_dir) / "t2.db"
        t3 = Path(temp_dir) / "t3.json"
        t4 = Path(temp_dir) / "vault"
        
        mem = UnifiedMemoryManager(tier1_dir=t1, tier2_db=t2, tier3_profile=t3, tier4_vault=t4)
        
        user_msg = Message(role=MessageRole.USER, content="I love Obsidian second brain workflows and Python microservices.")
        assistant_msg = Message(role=MessageRole.ASSISTANT, content="Understood! I will log notes to Obsidian and focus on Python.")
        
        mem.record_interaction("sess_integration", user_msg, assistant_msg)
        
        context = mem.build_augmented_context("sess_integration", "Obsidian")
        assert "TIER 1 CORE MEMORY" in context
        assert "TIER 3 COGNITIVE INSIGHTS" in context
        assert "TIER 2 EPISODIC RECALL" in context
        
        # Explicitly close SQLite connection to release file lock on Windows
        mem.tier2.close()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
