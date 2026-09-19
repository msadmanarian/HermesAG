import tempfile
import shutil
from pathlib import Path
from hermes.memory.tier1_core import Tier1CoreMemory

def test_tier1_core_lifecycle():
    temp_dir = tempfile.mkdtemp()
    try:
        t1 = Tier1CoreMemory(temp_dir)
        assert (Path(temp_dir) / "soul.md").exists()
        assert (Path(temp_dir) / "user.md").exists()
        assert (Path(temp_dir) / "memory.md").exists()
        
        # Test adding fact
        t1.add_fact("Hermes is running on Python 3.14")
        assert "Hermes is running on Python 3.14" in t1.system_memory.facts
        
        # Test persistence
        t1_reloaded = Tier1CoreMemory(temp_dir)
        assert "Hermes is running on Python 3.14" in t1_reloaded.system_memory.facts
        
        context = t1.render_system_prompt_context()
        assert "TIER 1 CORE MEMORY" in context
        assert "Hermes is running on Python 3.14" in context
    finally:
        shutil.rmtree(temp_dir)
