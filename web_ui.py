import os, glob, json, asyncio, subprocess
from datetime import datetime
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

import agents.base
agents.base.BaseAgent.log_event = lambda self, event_type, data: broadcast(event_type, data)

# ==========================================
# زمان‌بند خودکار (Lazy Cron)
# ==========================================
async def scheduled_runner():
    while True:
        now = datetime.now()
        # اگر ساعت ۲:۱۵ بامداد گذشته باشد
        if now.hour > 2 or (now.hour == 2 and now.minute >= 15):
            today_str = now.strftime("%Y-%m-%d")
            last_run_file = "last_run.txt"
            
            # چک کردن اینکه آیا امروز اجرا شده یا نه
            has_run_today = False
            if os.path.exists(last_run_file):
                with open(last_run_file, "r") as f:
                    if f.read().strip() == today_str:
                        has_run_today = True
            
            if not has_run_today:
                print(f"🚀 [Scheduler] شروع ماموریت خودکار شبانه برای تاریخ {today_str}")
                with open(last_run_file, "w") as f:
                    f.write(today_str)
                
                # خواندن هدف از فایل
                if os.path.exists("goal.txt"):
                    # اجرای اسکریپت خودمختار در یک پروسه جداگانه
                    subprocess.run(["python3", "autonomous_runner.py", "goal.txt"])
                else:
                    print("⚠️ [Scheduler] فایل goal.txt پیدا نشد.")
                    
        await asyncio.sleep(60) # هر ۱ دقیقه چک میکنه

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scheduled_runner())

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
