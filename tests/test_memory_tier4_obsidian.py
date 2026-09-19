import tempfile
import shutil
from pathlib import Path
from hermes.memory.tier4_obsidian import Tier4ObsidianVault
from hermes.memory.tier4_prd import ObsidianPRDManager

def test_obsidian_vault_and_prd():
    temp_dir = tempfile.mkdtemp()
    try:
        vault = Tier4ObsidianVault(temp_dir)
        prd_mgr = ObsidianPRDManager(vault)
        
        # Test PRD Creation
        prd_path = prd_mgr.create_prd(
            title="Floating Pomodoro App",
            problem_statement="User needs an unobtrusive floating timer that integrates with Obsidian.",
            user_stories=["As a user, I can start a 25-minute timer", "As a user, my sessions log to Obsidian"],
            technical_spec="Built using PySide6 or Tkinter with local Obsidian Markdown file appends."
        )
        assert prd_path.exists()
        content = prd_path.read_text(encoding="utf-8")
        assert "Floating Pomodoro App" in content
        assert "25-minute timer" in content
        
        # Test Daily Note
        log_path = prd_mgr.append_daily_log("Executed 10 tasks and synced memory.")
        assert log_path.exists()
        log_content = log_path.read_text(encoding="utf-8")
        assert "Executed 10 tasks" in log_content
    finally:
        shutil.rmtree(temp_dir)
