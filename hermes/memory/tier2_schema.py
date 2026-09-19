SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata_json TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    tool_calls_json TEXT,
    tool_results_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
"""

FTS5_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS fts_messages USING fts5(
    session_id UNINDEXED,
    role UNINDEXED,
    content,
    tokenize = 'porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS trg_messages_ai AFTER INSERT ON messages
BEGIN
    INSERT INTO fts_messages(session_id, role, content)
    VALUES (new.session_id, new.role, new.content);
END;

CREATE TRIGGER IF NOT EXISTS trg_messages_ad AFTER DELETE ON messages
BEGIN
    DELETE FROM fts_messages WHERE session_id = old.session_id AND content = old.content;
END;
"""
