# The 4-Tier Memory Architecture

HermesAG separates cognitive state into four distinct, hierarchically indexed tiers:

1. **Tier 1: Core Files (`memory.md`, `user.md`, `soul.md`)**
   - Direct prompt injection for stable persona, identity, and mission invariants.
2. **Tier 2: Episodic SQLite Memory with FTS5**
   - Fast full-text lexical search across conversation history.
3. **Tier 3: Cognitive Pattern Profiler (Honcho-style)**
   - Distills implicit user preferences and habits without manual configuration.
4. **Tier 4: Second Brain Integration (Obsidian Vault)**
   - Syncs Product Requirement Documents (PRDs), notes, and logs to local Markdown vaults.
