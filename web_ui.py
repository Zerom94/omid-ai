#!/usr/bin/env python3
"""OMID AI — Web Dashboard Backend

FastAPI server that serves the UI and provides SSE-based real-time log
streaming. Connects to core.manager so the Manager Agent orchestrates the
mission on demand.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from agents.base import BaseAgent, Task, Result
from core.manager import ManagerAgent
from core.task_queue import TaskQueue
from core.memory import MemoryStore

AGENT_NAMES = [
    "Manager", "Research", "Developer", "Analyst",
    "Security", "Testing", "Automation", "Memory", "Quality Control",
]

STATUS_LISTENERS = {
    "pending":     {"label": "Idle",   "color": "text-gray-400",   "bg": "bg-gray-500"},
    "in_progress": {"label": "Working","color": "text-cyan-400",   "bg": "bg-cyan-500"},
    "verified":    {"label": "Done",   "color": "text-green-600",   "bg": "bg-green-500"},
    "failed":      {"label": "Failed", "color": "text-red-400",     "bg": "bg-red-500"},
    "dead":        {"label": "Dead",   "color": "text-amber-400",   "bg": "bg-amber-500"},
}


class MissionGoal(BaseModel):
    goal: str


_RUNTIME = {
    "manager": None,
    "task_queue": None,
    "memory": None,
    "sse_queues": [],      # list of asyncio.Queue for each connected SSE client
    "is_busy": False,
}


def _build_manager():
    config = {}
    memory = MemoryStore()
    task_queue = TaskQueue(max_retries=3)
    manager = ManagerAgent(task_queue=task_queue, memory=memory, config=config)
    return manager, task_queue, memory


def _register_broadcast(callback) -> None:
    """Register a log callback so all agents broadcast events to SSE clients."""
    BaseAgent.log_callback = callback


def _sse_payload(payload) -> str:
    """Build an SSE event-stream payload line."""
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


async def _broadcast_all(msg: str | dict) -> None:
    """Push a payload to every active SSE client queue."""
    if isinstance(msg, str):
        data_str = msg
    else:
        data_str = json.dumps(msg, ensure_ascii=False)
    sse_line = f"data: {data_str}\n\n"
    for q in list(_RUNTIME["sse_queues"]):
        try:
            await q.put(sse_line)
        except Exception:
            _RUNTIME["sse_queues"].remove(q)


def _flush_state() -> dict:
    """Return the current task queue snapshot."""
    tq = _RUNTIME["task_queue"]
    if tq is None:
        return {}
    counts = {"total": len(tq._tasks), "by_status": {}}
    for task in tq._tasks.values():
        st = task.task.status
        counts["by_status"][st] = counts["by_status"].get(st, 0) + 1
    return {"queue": counts}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _RUNTIME
    _RUNTIME["manager"], _RUNTIME["task_queue"], _RUNTIME["memory"] = _build_manager()
    # Register broadcast callback so all agents stream to SSE clients
    BaseAgent.log_callback = lambda event_type, data: _broadcast_all({
        "type": "log",
        "message": f"[{event_type}] {data.get('task_id', '')}: {data.get('error', data.get('agent', ''))}".strip(),
        "level": "error" if event_type in ("fail", "crash") else "info",
    })
    yield


app = FastAPI(title="OMID AI Dashboard", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Root: serve the dashboard HTML via FileResponse
# ---------------------------------------------------------------------------
@app.get("/")
async def index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(index_path)


# ---------------------------------------------------------------------------
# POST /api/mission  — submit a Mission Goal to the Manager
# ---------------------------------------------------------------------------
@app.post("/api/mission")
async def post_mission(payload: MissionGoal):
    goal = payload.goal
    if not goal or not goal.strip():
        return JSONResponse({"error": "goal is required"}, status_code=422)

    run_id = "m_" + str(int(time.time() * 1000))
    _RUNTIME["manager"].log_event("new_mission", {
        "run_id": run_id,
        "goal": goal,
    })
    await _broadcast_all(f"🚀 Mission submitted (run #{run_id}):\n\n> {goal}\n\nManager Agent has been notified.")
    _RUNTIME["is_busy"] = True
    try:
        results = await _RUNTIME["manager"].plan_and_dispatch(goal)
    except Exception as exc:
        await _broadcast_all(f"⚠️ Mission crashed: {exc}")
        results = []
    finally:
        _RUNTIME["is_busy"] = False

    summary = []
    for i, r in enumerate(results):
        tag = "✅" if r and r.success else "❌"
        detail = r.output if r and r.success else (r.error or "error")
        summary.append({
            "index": i,
            "success": bool(r and r.success),
            "task_id": r.task_id if r else "",
            "description": getattr(r, "description", "") if r else "",
            "output_preview": str(detail)[:120],
            "execution_ms": r.execution_time_ms if r else 0,
            "timestamp": r.timestamp if r else "",
        })
    await _broadcast_all(
        f"Mission summary: {'✅ ' + str(len([r for r in results if r and r.success])) + ' tasks succeeded, ' + str(len([r for r in results if not (r and r.success)])) + ' failed.'}"
    )
    final = json.dumps({"type": "final", "summary": summary})
    await _broadcast_all(final)
    await _broadcast_all(json.dumps({"type": "done"}))
    return JSONResponse({
        "status": "completed",
        "mission_id": run_id,
        "results": summary,
    })


# ---------------------------------------------------------------------------
# GET /api/state  — current agent status snapshot
# ---------------------------------------------------------------------------
@app.get("/api/state")
async def get_state():
    snap = _flush_state()
    return snap


# ---------------------------------------------------------------------------
# GET /api/health
# ---------------------------------------------------------------------------
@app.get("/api/health")
async def health():
    return {"status": "ok", "agents": len(AGENT_NAMES)}


# ---------------------------------------------------------------------------
# SSE: GET /sse  — stream live logs via Server-Sent Events
# ---------------------------------------------------------------------------
@app.get("/sse")
async def sse_endpoint():
    """Return an SSE stream. Each broadcast pushes one data line to all queues."""
    client_queue: asyncio.Queue[str] = asyncio.Queue()
    _RUNTIME["sse_queues"].append(client_queue)

    async def gen():
        try:
            # Send initial state snapshot
            initial = _flush_state()
            yield f"data: {json.dumps({'type': 'init', 'queue': initial}, ensure_ascii=False)}\n\n"

            while True:
                try:
                    msg = await asyncio.wait_for(client_queue.get(), timeout=2.0)
                    yield msg
                except asyncio.TimeoutError:
                    # Heartbeat to keep connection alive
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if client_queue in _RUNTIME["sse_queues"]:
                _RUNTIME["sse_queues"].remove(client_queue)

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# Register the broadcast helper so it is available before any route runs.
app.state.broadcast = _broadcast_all


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)