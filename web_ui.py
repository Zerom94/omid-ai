import os
import glob
import json
import asyncio
import subprocess
import logging
import traceback
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.manager import ManagerAgent
from core.memory import MemoryStore

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sse_queues: list[asyncio.Queue] = []

class MissionGoal(BaseModel):
    goal: str

def broadcast(event_type: str, data: dict) -> None:
    print(f"[DASHBOARD] {event_type} -> {data}", flush=True)
    if not isinstance(data, dict):
        data = {"message": str(data)}
    for q in sse_queues:
        q.put_nowait({"type": event_type, "data": data})

import agents.base
def custom_log_event(self, event_type, data):
    print(f"[LOG] {data.get('agent', 'System')}: {data.get('status', '')}", flush=True)
    broadcast(event_type, data)
agents.base.BaseAgent.log_event = custom_log_event

@app.get("/")
async def index() -> FileResponse:
    return FileResponse("index.html")

async def run_mission(goal: str):
    try:
        print(f"\n--> [MISSION STARTED] {goal}", flush=True)
        broadcast("working", {"agent": "Manager", "status": "Planning tasks..."})
        memory = MemoryStore()
        manager = ManagerAgent(config={}, memory=memory)
        await manager.plan_and_dispatch(goal)
        print("--> [MISSION FINISHED]", flush=True)
        
        # 👇 این خط مهم‌ترین بخش است: ارسال سیگنال پایان کل کارها
        broadcast("all_tasks_done", {"agent": "System", "status": "Complete"})
        
    except Exception as e:
        traceback.print_exc()
        broadcast("fail", {"agent": "Manager", "status": f"Error: {str(e)}"})

@app.post("/api/mission")
async def post_mission(payload: MissionGoal) -> dict:
    asyncio.create_task(run_mission(payload.goal))
    return {"status": "started"}

@app.get("/api/files")
async def get_files() -> dict:
    files = glob.glob("src/**/*.py", recursive=True)
    # مرتب‌سازی بر اساس زمان تغییر (جدیدترین‌ها اول)
    files.sort(key=os.path.getmtime, reverse=True)
    files = files[:30] # فقط ۳۰ فایل آخر
    return {"files": [os.path.relpath(f, "src") for f in files]}

@app.get("/api/file/{filename:path}")
async def get_file(filename: str) -> dict:
    try:
        with open(os.path.join("src", filename), "r") as f:
            return {"code": f.read()}
    except Exception:
        return {"code": "# File not found"}

@app.get("/api/reports")
async def get_reports() -> dict:
    report_dir = "/sdcard/omid-ai/security_scans"
    if not os.path.exists(report_dir):
        return {"reports": []}
    files = [f for f in os.listdir(report_dir) if f.endswith('.md')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(report_dir, x)), reverse=True)
    return {"reports": files}

@app.get("/api/reports/{filename}")
async def get_report_content(filename: str) -> dict:
    if ".." in filename or "/" in filename:
        return {"error": "Invalid filename"}
    file_path = f"/sdcard/omid-ai/security_scans/{filename}"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    return {"error": "Report not found"}



@app.delete("/api/files/{filename:path}")
async def delete_project_file(filename: str) -> dict:
    file_path = os.path.join("src", filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
    return {"status": "error", "detail": "File not found"}

@app.get("/sse")
async def sse_endpoint():
    queue: asyncio.Queue = asyncio.Queue()
    sse_queues.append(queue)
    async def gen():
        try:
            while True:
                try:
                    msg = await asyncio.wait_for(queue.get(), timeout=10.0)
                    yield f"data: {json.dumps(msg)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in sse_queues:
                sse_queues.remove(queue)
    return StreamingResponse(gen(), media_type="text/event-stream")
