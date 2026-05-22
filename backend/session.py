from __future__ import annotations

import asyncio
import json
import sqlite3
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import SessionInfo, SyscallEvent

DB_PATH = Path(__file__).parent.parent / "data" / "sessions.db"


def _init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            command TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            total_syscalls INTEGER DEFAULT 0,
            status TEXT DEFAULT 'running'
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            pid INTEGER,
            timestamp TEXT,
            syscall TEXT,
            args TEXT,
            result TEXT,
            duration REAL,
            category TEXT,
            severity TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        );
        CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
    """
    )
    conn.close()


_init_db()


class SessionStore:
    def __init__(self):
        self._conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    def create_session(self, command: str) -> str:
        session_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        self._conn.execute(
            "INSERT INTO sessions (id, command, start_time, status) VALUES (?, ?, ?, ?)",
            (session_id, command, now, "running"),
        )
        self._conn.commit()
        return session_id

    def finish_session(self, session_id: str, total: int, status: str = "finished"):
        now = datetime.now().isoformat()
        self._conn.execute(
            "UPDATE sessions SET end_time=?, total_syscalls=?, status=? WHERE id=?",
            (now, total, status, session_id),
        )
        self._conn.commit()

    def save_events_batch(self, session_id: str, events: list[SyscallEvent]):
        rows = [
            (
                session_id,
                e.pid,
                e.timestamp,
                e.syscall,
                e.args,
                e.result,
                e.duration,
                e.category.value,
                e.severity.value,
            )
            for e in events
        ]
        self._conn.executemany(
            "INSERT INTO events (session_id, pid, timestamp, syscall, args, result, duration, category, severity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
        self._conn.commit()

    def list_sessions(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM sessions ORDER BY start_time DESC LIMIT 50"
        ).fetchall()
        return [dict(r) for r in rows]

    def get_session(self, session_id: str) -> Optional[dict]:
        row = self._conn.execute(
            "SELECT * FROM sessions WHERE id=?", (session_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_events(
        self, session_id: str, limit: int = 1000, offset: int = 0
    ) -> list[dict]:
        rows = self._conn.execute(
            "SELECT * FROM events WHERE session_id=? ORDER BY id LIMIT ? OFFSET ?",
            (session_id, limit, offset),
        ).fetchall()
        return [dict(r) for r in rows]


store = SessionStore()
