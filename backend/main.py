from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .analyzer import assess_severity, classify_syscall
from .models import StartRequest, SyscallEvent
from .parser import StraceParser
from .runner import StraceRunner
from .session import store
from .websocket import manager

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

active_runners: dict[str, StraceRunner] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    for runner in active_runners.values():
        await runner.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/api/start")
async def start_trace(req: StartRequest):
    session_id = store.create_session(req.command)
    runner = StraceRunner()
    active_runners[session_id] = runner
    asyncio.create_task(_run_trace(session_id, runner, req.command))
    return {"session_id": session_id, "status": "started"}


@app.post("/api/stop/{session_id}")
async def stop_trace(session_id: str):
    runner = active_runners.get(session_id)
    if runner and runner.is_running:
        await runner.stop()
        return {"status": "stopped"}
    return JSONResponse({"error": "session not found or not running"}, status_code=404)


@app.get("/api/sessions")
async def list_sessions():
    return store.list_sessions()


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    s = store.get_session(session_id)
    if not s:
        return JSONResponse({"error": "not found"}, status_code=404)
    return s


@app.get("/api/sessions/{session_id}/events")
async def get_events(session_id: str, limit: int = 1000, offset: int = 0):
    return store.get_events(session_id, limit, offset)


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(session_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(session_id, websocket)


async def _run_trace(session_id: str, runner: StraceRunner, command: str):
    parser = StraceParser()
    event_id = 0
    batch: list[dict] = []
    db_batch: list[SyscallEvent] = []
    stats = {
        "total_count": 0,
        "category_counts": {},
        "syscall_counts": {},
        "top_slow": [],
    }

    try:
        await manager.send_status(session_id, "running")
        async for line in runner.start(command):
            raw = parser.parse_line(line)
            if raw is None:
                continue

            event_id += 1
            category = classify_syscall(raw.syscall)
            severity = assess_severity(raw.duration)

            event = SyscallEvent(
                id=event_id,
                pid=raw.pid,
                timestamp=raw.timestamp,
                syscall=raw.syscall,
                args=raw.args,
                result=raw.result,
                duration=raw.duration,
                category=category,
                severity=severity,
            )

            event_dict = {
                "id": event.id,
                "pid": event.pid,
                "timestamp": event.timestamp,
                "syscall": event.syscall,
                "args": event.args,
                "result": event.result,
                "duration": event.duration,
                "category": event.category.value,
                "severity": event.severity.value,
            }

            batch.append(event_dict)
            db_batch.append(event)

            stats["total_count"] += 1
            stats["category_counts"][category.value] = (
                stats["category_counts"].get(category.value, 0) + 1
            )
            stats["syscall_counts"][raw.syscall] = (
                stats["syscall_counts"].get(raw.syscall, 0) + 1
            )

            if event.duration and event.duration > 0.01:
                stats["top_slow"].append(event_dict)
                stats["top_slow"].sort(
                    key=lambda x: x.get("duration") or 0, reverse=True
                )
                stats["top_slow"] = stats["top_slow"][:20]

            if len(batch) >= 50:
                await manager.send_event_batch(session_id, batch)
                await manager.send_stats(session_id, stats)
                batch = []

            if len(db_batch) >= 200:
                store.save_events_batch(session_id, db_batch)
                db_batch = []

        if batch:
            await manager.send_event_batch(session_id, batch)
        if db_batch:
            store.save_events_batch(session_id, db_batch)

        await manager.send_stats(session_id, stats)
        await manager.send_status(session_id, "finished")
        store.finish_session(session_id, event_id, "finished")

    except Exception as e:
        await manager.send_status(session_id, "error", str(e))
        store.finish_session(session_id, event_id, "error")
    finally:
        active_runners.pop(session_id, None)


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
