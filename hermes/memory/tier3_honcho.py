import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from hermes.core.types import Message, MessageRole
from hermes.memory.tier3_schema import UserCognitiveProfile, CognitivePattern

STOP_WORDS = {"the", "a", "an", "is", "are", "and", "or", "in", "on", "for", "with", "this", "that", "it", "to", "of"}

class Tier3CognitiveTracker:
    """
    Tier 3 Memory: Honcho-style implicit behavioral and preference engine.
    Observes ongoing user conversations to distill implicit preferences without requiring explicit prompts.
    """
    def __init__(self, profile_path: str | Path = "data/tier3_profile.json"):
        self.profile_path = Path(profile_path)
        self.profile = self._load_profile()

    def _load_profile(self) -> UserCognitiveProfile:
        if self.profile_path.exists():
            try:
                data = json.loads(self.profile_path.read_text(encoding="utf-8"))
                return UserCognitiveProfile(**data)
            except Exception:
                pass
        return UserCognitiveProfile()

    def save(self):
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        self.profile_path.write_text(
            self.profile.model_dump_json(indent=2),
            encoding="utf-8"
        )

    def observe_message(self, message: Message):
        if message.role != MessageRole.USER:
            return
        content = message.content.lower()
        
        # 1. Extract and cluster interest keywords
        words = re.findall(r'\b[a-z]{3,15}\b', content)
        for w in words:
            if w not in STOP_WORDS:
                self.profile.interest_keywords[w] = self.profile.interest_keywords.get(w, 0) + 1

        # 2. Heuristic pattern observation
        if "pomodoro" in content or "timer" in content:
            self._reinforce_pattern("time_management", "work_rhythm", "Values focused intervals and pomodoro timing techniques")
        if "fastapi" in content or "python" in content:
            self._reinforce_pattern("python_preference", "tool_bias", "Prefers modern Python/FastAPI async architectures")
        if "concise" in content or "no fluff" in content or "quick" in content:
            self._reinforce_pattern("concise_communication", "communication", "Strong preference for direct, high-density outputs")

        self.save()

    def _reinforce_pattern(self, pattern_id: str, category: str, description: str):
        if pattern_id in self.profile.patterns:
            p = self.profile.patterns[pattern_id]
            p.evidence_count += 1
            p.confidence = min(1.0, p.confidence + 0.1)
        else:
            self.profile.patterns[pattern_id] = CognitivePattern(
                pattern_id=pattern_id,
                category=category,
                description=description,
                confidence=0.6,
                evidence_count=1
            )

    def get_top_interests(self, top_n: int = 5) -> List[tuple[str, int]]:
        return sorted(self.profile.interest_keywords.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def render_tier3_context(self) -> str:
        patterns_str = "\n".join(
            f"- [{p.category.upper()}] {p.description} (confidence: {p.confidence:.1f})"
            for p in self.profile.patterns.values() if p.confidence >= 0.6
        )
        return f"""=== TIER 3 COGNITIVE INSIGHTS (HONCHO) ===
{patterns_str if patterns_str else '- No high-confidence implicit patterns detected yet.'}
Top Interests: {', '.join(k for k, _ in self.get_top_interests())}
======================================="""
