from agents.base import BaseAgent, Task, Result
import glob

class QualityControlAgent(BaseAgent):
    name = "QualityControl"
    display_name = "Quality Control"

    async def execute(self, task: Task) -> Result:
        # یک بررسی ساده: آیا فایلی ساخته شده است؟
        files = glob.glob("src/**/*.py", recursive=True)
        if files:
            print(f"✅ [QC] Found {len(files)} generated files. Passed.")
            return Result(task_id=task.id, success=True, output={"status": "verified"})
        else:
            print(f"❌ [QC] No files found to verify.")
            return Result(task_id=task.id, success=False, error="No files found")
