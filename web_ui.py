import os, shutil, glob, json, asyncio
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.manager import ManagerAgent
from core.memory import MemoryStore

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

sse_queues = []

class MissionGoal(BaseModel):
    goal: str

def broadcast(event_type: str, data: dict):
    for q in sse_queues:
        q.put_nowait({"type": event_type, "data": data})

# اتصال سیستم لاگ ایجنت‌ها به SSE
import agents.base
agents.base.BaseAgent.log_event = lambda self, event_type, data: broadcast(event_type, data)

@app.get("/")
async def index():
    return FileResponse("index.html")

@app.post("/api/mission")
async def post_mission(payload: MissionGoal):
    memory = MemoryStore()
    manager = ManagerAgent(config={}, memory=memory)
    asyncio.create_task(manager.plan_and_dispatch(payload.goal))
    return {"status": "started"}

@app.get("/api/files")
async def get_files():
    files = glob.glob("src/**/*.py", recursive=True)
    return {"files": [os.path.relpath(f, "src") for f in files]}

@app.get("/api/file/{filename:path}")
async def get_file(filename: str):
    try:
        with open(os.path.join("src", filename), "r") as f:
            return {"code": f.read()}
    except: return {"code": "# File not found"}

@app.get("/api/download/{filename:path}")
async def download_file(filename: str):
    path = os.path.join("src", filename)
    if os.path.exists(path):
        return FileResponse(path, media_type='text/x-python', filename=os.path.basename(filename))
    return {"error": "Not found"}


import shutil
@app.get("/api/download_zip/{folder_name}")
async def download_zip(folder_name: str):
    folder_path = os.path.join("src", folder_name)
    if not os.path.isdir(folder_path):
        return {"error": "Folder not found"}
    zip_filename = f"{folder_name}.zip"
    zip_path = os.path.join("src", zip_filename)
    shutil.make_archive(os.path.join("src", folder_name), 'zip', folder_path)
    return FileResponse(zip_path, media_type='application/zip', filename=zip_filename)

@app.get("/sse")
async def sse_endpoint():
    queue = asyncio.Queue()
    sse_queues.append(queue)
    
    async def gen():
        try:
            while True:
                msg = await queue.get()
                yield f"data: {json.dumps(msg)}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in sse_queues: sse_queues.remove(queue)
            
    return StreamingResponse(gen(), media_type="text/event-stream")
