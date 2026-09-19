from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from hermes.memory.tier4_obsidian import Tier4ObsidianVault

class ObsidianPRDManager:
    """
    Automates generating and linking Product Requirement Documents (PRDs) inside the Obsidian Second Brain.
    """
    def __init__(self, vault: Tier4ObsidianVault):
        self.vault = vault

    def create_prd(
        self,
        title: str,
        problem_statement: str,
        user_stories: List[str],
        technical_spec: str,
        tags: List[str] | None = None
    ) -> Path:
        slug = title.lower().replace(" ", "-")
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        frontmatter = {
            "title": f'"{title}"',
            "created": date_str,
            "type": "prd",
            "tags": tags or ["hermes", "prd", "architecture"],
            "status": "draft"
        }

        stories_md = "\n".join(f"- [ ] {s}" for s in user_stories)
        body = f"""# {title}

## 1. Problem Statement & Objective
{problem_statement}

## 2. User Stories & Acceptance Criteria
{stories_md}

## 3. Technical Architecture & Implementation Details
{technical_spec}

---
*Created autonomously via HermesAG Tier 4 Obsidian Integration*
"""
        rel_path = f"PRDs/{slug}.md"
        return self.vault.write_note(rel_path, body, frontmatter)

    def append_daily_log(self, summary: str, tags: List[str] | None = None) -> Path:
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        rel_path = f"Daily Notes/{today_str}.md"
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        
        existing = self.vault.read_note(rel_path) or f"# Daily Briefing & Work Log — {today_str}\n\n"
        entry = f"""
### [{timestamp}] Hermes Activity
{summary}
"""
        updated = existing + entry
        return self.vault.write_note(rel_path, updated)
