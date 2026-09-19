import tempfile
from pathlib import Path
from hermes.core.types import Message, MessageRole
from hermes.memory.tier3_honcho import Tier3CognitiveTracker

def test_tier3_cognitive_tracker():
    temp_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()

    try:
        tracker = Tier3CognitiveTracker(temp_path)
        tracker.observe_message(Message(role=MessageRole.USER, content="I want to build a Pomodoro timer using FastAPI and Python. Keep it concise!"))
        
        top_interests = [w for w, _ in tracker.get_top_interests(10)]
        assert "pomodoro" in top_interests or "fastapi" in top_interests or "python" in top_interests
        assert "time_management" in tracker.profile.patterns
        assert tracker.profile.patterns["time_management"].confidence >= 0.6
        
        ctx = tracker.render_tier3_context()
        assert "TIER 3 COGNITIVE INSIGHTS" in ctx
        assert "pomodoro" in ctx.lower()
    finally:
        if temp_path.exists():
            temp_path.unlink()
