import tempfile
from pathlib import Path
from hermes.core.types import Message, MessageRole
from hermes.memory.tier2_sqlite import Tier2SessionMemory

def test_tier2_sqlite_session_and_search():
    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()

    try:
        mem = Tier2SessionMemory(temp_path)
        mem.create_session("sess_1", "Project Discussion")
        
        msg1 = Message(role=MessageRole.USER, content="Can we build a floating Pomodoro application?")
        msg2 = Message(role=MessageRole.ASSISTANT, content="Yes, we can build it using Python or Swift and sync with Obsidian.")
        
        mem.log_message("sess_1", msg1)
        mem.log_message("sess_1", msg2)
        
        history = mem.get_session_history("sess_1")
        assert len(history) == 2
        assert history[0].role == MessageRole.USER
        assert "Pomodoro" in history[0].content
        
        # Test full-text search
        results = mem.search("Pomodoro")
        assert len(results) >= 1
        assert results[0]["session_id"] == "sess_1"
        mem.close()
    finally:
        if temp_path.exists():
            temp_path.unlink()
