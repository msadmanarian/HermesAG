import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

class Tier4ObsidianVault:
    """
    Tier 4 Memory: Second Brain Integration via Obsidian Vault.
    Syncs notes, product requirement documents (PRDs), and daily logs into standard Markdown files with frontmatter.
    """
    def __init__(self, vault_path: str | Path):
        self.vault_path = Path(vault_path)
        self.daily_notes_dir = self.vault_path / "Daily Notes"
        self.prds_dir = self.vault_path / "PRDs"
        self.projects_dir = self.vault_path / "Projects"
        self._ensure_dirs()

    def _ensure_dirs(self):
        self.daily_notes_dir.mkdir(parents=True, exist_ok=True)
        self.prds_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def write_note(self, relative_path: str, content: str, frontmatter: Optional[Dict[str, Any]] = None) -> Path:
        target = self.vault_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        
        text = ""
        if frontmatter:
            text += "---\n"
            for k, v in frontmatter.items():
                text += f"{k}: {v}\n"
            text += "---\n\n"
        text += content
        target.write_text(text, encoding="utf-8")
        return target

    def read_note(self, relative_path: str) -> Optional[str]:
        target = self.vault_path / relative_path
        if target.exists():
            return target.read_text(encoding="utf-8")
        return None

    def list_notes(self, subfolder: str = "") -> List[str]:
        folder = self.vault_path / subfolder if subfolder else self.vault_path
        if not folder.exists():
            return []
        return [str(p.relative_to(self.vault_path)).replace("\\", "/") for p in folder.rglob("*.md")]
