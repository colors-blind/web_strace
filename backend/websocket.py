from __future__ import annotations

import asyncio
import json
import time
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect

from .models import SessionStats, SyscallEvent

BATCH_INTERVAL = 0.05
BATCH_MAX_SIZE = 100
STATS_INTERVAL = 0.5


class ConnectionManager:
    def __init__(self):
        self._connections: dict[str, list[WebSocket]] = {}
        self._event_queues: dict[str, asyncio.Queue] = {}

    async def connect(self, session_id: str, ws: WebSocket):
        await ws.accept()
        if session_id not in self._connections:
            self._connections[session_id] = []
        self._connections[session_id].append(ws)

    def disconnect(self, session_id: str, ws: WebSocket):
        if session_id in self._connections:
            self._connections[session_id] = [
                c for c in self._connections[session_id] if c is not ws
            ]
            if not self._connections[session_id]:
                del self._connections[session_id]

    def get_queue(self, session_id: str) -> asyncio.Queue:
        if session_id not in self._event_queues:
            self._event_queues[session_id] = asyncio.Queue()
        return self._event_queues[session_id]

    def remove_queue(self, session_id: str):
        self._event_queues.pop(session_id, None)

    async def broadcast(self, session_id: str, message: dict):
        connections = self._connections.get(session_id, [])
        data = json.dumps(message)
        disconnected = []
        for ws in connections:
            try:
                await ws.send_text(data)
            except (WebSocketDisconnect, RuntimeError):
                disconnected.append(ws)
        for ws in disconnected:
            self.disconnect(session_id, ws)

    async def send_event_batch(self, session_id: str, events: list[dict]):
        if not events:
            return
        await self.broadcast(session_id, {"type": "batch", "data": events})

    async def send_stats(self, session_id: str, stats: dict):
        await self.broadcast(session_id, {"type": "stats", "data": stats})

    async def send_status(self, session_id: str, state: str, message: str = ""):
        await self.broadcast(
            session_id,
            {"type": "status", "data": {"state": state, "message": message}},
        )


manager = ConnectionManager()
