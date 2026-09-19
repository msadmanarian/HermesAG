import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from hermes.core.types import Message, MessageRole, ToolCall, ToolResult
from hermes.memory.tier2_schema import SCHEMA_V1, FTS5_SCHEMA

class Tier2SessionMemory:
    """
    Tier 2 Memory: High-performance SQLite episodic conversation store with FTS5 lexical full-text indexing.
    """
    def __init__(self, db_path: str | Path = ":memory:"):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.executescript(SCHEMA_V1)
            try:
                self.conn.executescript(FTS5_SCHEMA)
                self.fts_enabled = True
            except sqlite3.OperationalError:
                self.fts_enabled = False

    def create_session(self, session_id: str, title: str = "New Session", metadata: Dict[str, Any] | None = None):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO sessions (session_id, title, metadata_json) VALUES (?, ?, ?)",
                (session_id, title, json.dumps(metadata or {}))
            )

    def log_message(self, session_id: str, message: Message):
        self.create_session(session_id)
        tool_calls = [tc.model_dump() for tc in message.tool_calls] if message.tool_calls else None
        tool_results = [tr.model_dump() for tr in message.tool_results] if message.tool_results else None
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO messages (session_id, role, content, tool_calls_json, tool_results_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    message.role.value,
                    message.content,
                    json.dumps(tool_calls) if tool_calls else None,
                    json.dumps(tool_results) if tool_results else None,
                )
            )

    def get_session_history(self, session_id: str, limit: int = 50) -> List[Message]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role, content, tool_calls_json, tool_results_json FROM messages WHERE session_id = ? ORDER BY id ASC LIMIT ?",
            (session_id, limit)
        )
        messages = []
        for row in cursor.fetchall():
            tc = [ToolCall(**item) for item in json.loads(row["tool_calls_json"])] if row["tool_calls_json"] else None
            tr = [ToolResult(**item) for item in json.loads(row["tool_results_json"])] if row["tool_results_json"] else None
            messages.append(Message(
                role=MessageRole(row["role"]),
                content=row["content"],
                tool_calls=tc,
                tool_results=tr
            ))
        return messages

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Searches past messages using FTS5 or fallback LIKE search."""
        cursor = self.conn.cursor()
        clean_query = query.replace('"', '""').replace("'", "''")
        if self.fts_enabled:
            try:
                cursor.execute(
                    """
                    SELECT session_id, role, snippet(fts_messages, 2, '<b>', '</b>', '...', 15) as snippet
                    FROM fts_messages
                    WHERE fts_messages MATCH ?
                    LIMIT ?
                    """,
                    (clean_query, limit)
                )
                return [{"session_id": r["session_id"], "role": r["role"], "snippet": r["snippet"]} for r in cursor.fetchall()]
            except sqlite3.OperationalError:
                pass
        
        # Fallback search
        cursor.execute(
            "SELECT session_id, role, content FROM messages WHERE content LIKE ? LIMIT ?",
            (f"%{query}%", limit)
        )
        return [{"session_id": r["session_id"], "role": r["role"], "snippet": r["content"][:100]} for r in cursor.fetchall()]

    def close(self):
        self.conn.close()
