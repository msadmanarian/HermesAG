from pathlib import Path
from typing import Optional
from hermes.memory.tier1_schema import SoulIdentity, UserProfile, SystemMemory

class Tier1CoreMemory:
    """
    Tier 1 Memory: High-priority core files (soul.md, user.md, memory.md).
    Loaded into every system prompt context for consistent identity and persona.
    """
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.soul_file = self.base_dir / "soul.md"
        self.user_file = self.base_dir / "user.md"
        self.memory_file = self.base_dir / "memory.md"
        
        self.soul = SoulIdentity()
        self.user = UserProfile()
        self.system_memory = SystemMemory()
        self.initialize_or_load()

    def initialize_or_load(self):
        if not self.soul_file.exists():
            self._save_soul()
        else:
            self._load_soul()

        if not self.user_file.exists():
            self._save_user()
        else:
            self._load_user()

        if not self.memory_file.exists():
            self._save_memory()
        else:
            self._load_memory()

    def _save_soul(self):
        directives = "\n".join(f"- {d}" for d in self.soul.core_directives)
        content = f"""# Soul Identity & Core Directives
**Name:** {self.soul.name}
**Persona:** {self.soul.persona}
**Voice:** {self.soul.voice}

## Core Directives
{directives}
"""
        self.soul_file.write_text(content, encoding="utf-8")

    def _load_soul(self):
        content = self.soul_file.read_text(encoding="utf-8")
        directives = []
        for line in content.splitlines():
            line_s = line.strip()
            if line_s.startswith("- "):
                directives.append(line_s[2:].strip())
        if directives:
            self.soul.core_directives = directives

    def _save_user(self):
        goals = "\n".join(f"- {g}" for g in self.user.long_term_goals)
        content = f"""# User Profile
**Name:** {self.user.name}
**Role:** {self.user.role}

## Long Term Goals
{goals}
"""
        self.user_file.write_text(content, encoding="utf-8")

    def _load_user(self):
        content = self.user_file.read_text(encoding="utf-8")
        goals = []
        for line in content.splitlines():
            line_s = line.strip()
            if line_s.startswith("- "):
                goals.append(line_s[2:].strip())
        if goals:
            self.user.long_term_goals = goals

    def _save_memory(self):
        facts = "\n".join(f"- {f}" for f in self.system_memory.facts)
        content = f"""# System Memory & Global Facts
## Known Facts
{facts if facts else '- No facts recorded yet.'}
"""
        self.memory_file.write_text(content, encoding="utf-8")

    def _load_memory(self):
        content = self.memory_file.read_text(encoding="utf-8")
        facts = []
        for line in content.splitlines():
            line_s = line.strip()
            if line_s.startswith("- ") and not line_s.startswith("- No facts"):
                facts.append(line_s[2:].strip())
        self.system_memory.facts = facts

    def add_fact(self, fact: str):
        if fact not in self.system_memory.facts:
            self.system_memory.facts.append(fact)
            self._save_memory()

    def render_system_prompt_context(self) -> str:
        """Assembles Tier 1 core context for inclusion into the LLM system prompt."""
        return f"""=== TIER 1 CORE MEMORY ===
[SOUL]
Name: {self.soul.name} | Role: {self.soul.persona}
Directives: {'; '.join(self.soul.core_directives)}

[USER]
Name: {self.user.name} ({self.user.role})
Goals: {'; '.join(self.user.long_term_goals)}

[CORE FACTS]
{chr(10).join(f'- {f}' for f in self.system_memory.facts) if self.system_memory.facts else 'None'}
========================"""
