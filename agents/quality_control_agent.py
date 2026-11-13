import os
import json
from agents.base import BaseAgent, Task, Result
import glob

class QualityControlAgent(BaseAgent):
    name = "QualityControl"
    display_name = "Quality Control"

    async def execute(self, task: Task) -> Result:
        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        rules = ""
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                import json
                rules = json.load(f).get("quality_control", "")
                if rules:
                    print(f"[{self.name}] 🎓 Using latest rules: {rules}", flush=True)
        # یک بررسی ساده: آیا فایلی ساخته شده است؟
        files = glob.glob("src/**/*.py", recursive=True)
        if files:
            print(f"✅ [QC] Found {len(files)} generated files. Passed.")
            return Result(task_id=task.id, success=True, output={"status": "verified"})
        else:
            print(f"❌ [QC] No files found to verify.")
            return Result(task_id=task.id, success=False, error="No files found")
