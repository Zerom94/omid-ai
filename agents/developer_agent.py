import os
import json
import glob
import httpx
import re
from json_repair import loads as repair_json
from agents.base import BaseAgent, Task, Result

class DeveloperAgent(BaseAgent):
    name = "Developer"
    display_name = "Software Developer"

    async def execute(self, task: Task) -> Result:
        os.makedirs("src", exist_ok=True)
        print(f"[Developer] 📝 Task: {task.description}", flush=True)

        # خواندن دانش جدید
        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        rules = ""
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                try:
                    kb = json.load(f)
                    rules = kb.get("developer", "")
                    if rules:
                        print(f"[Developer] 🎓 Using latest rules (simplified for this task).", flush=True)
                except Exception:
                    pass

        max_idx = max([int(os.path.basename(d).replace("project_", "")) for d in glob.glob("src/project_*") if os.path.isdir(d)] + [0])
        project_dir = f"src/project_{max_idx + 1:04d}"
        os.makedirs(project_dir, exist_ok=True)

        # پرامپت بسیار سخت‌گیرانه و ساده‌تر
        prompt = f"""You are an expert Python developer.
Your task is EXACTLY: {task.description}

CRITICAL INSTRUCTIONS:
1. You MUST write Python code that fulfills the exact task above.
2. Output ONLY valid JSON. Do NOT use markdown. Do NOT add any explanation.
3. The JSON MUST have this exact structure: {{"files": [{{"name": "main.py", "content": "python code here"}}]}}
4. You MUST include at least one file in the "files" array. Never return an empty list.
"""

        raw = await self.call_self(prompt)
        
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not match:
            return Result(task_id=task.id, success=False, output="No JSON found in response")

        try:
            data = repair_json(match.group(0))
            files = data.get("files", [])
            
            if not files:
                print(f"[Developer] ⚠️ AI returned empty files list. Forcing a fallback file.", flush=True)
                # اگر مدل باز هم تنبلی کرد، یک فایل پیش‌فرض می‌سازیم تا سیستم کرش نکند
                files = [{"name": "main.py", "content": "# AI failed to generate code. Please retry."}]
                
            final_main_code = "# No code generated."
            for f in files:
                fname = f.get("name", "main.py")
                fcontent = f.get("content", "")
                
                file_path = os.path.join(project_dir, fname)
                dir_path = os.path.dirname(file_path)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
                
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(fcontent)
                    
                if fname == "main.py":
                    final_main_code = fcontent
                    
            print(f"[Developer] ✅ فایل‌ها در {project_dir} ذخیره شدند.", flush=True)
            self.log_event("code_generated", {"filename": f"{project_dir}/main.py", "code": final_main_code})
            return Result(task_id=task.id, success=True)
            
        except Exception as e:
            print(f"[Developer] خطا در پردازش JSON: {e}", flush=True)
            return Result(task_id=task.id, success=False, output=str(e))

    async def call_self(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:5001/v1/chat/completions",
                    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]},
                    timeout=120.0
                )
                data = resp.json()
                if 'choices' in data: 
                    return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"خطا در اتصال به روتر: {e}", flush=True)
        return "{}"
