import os
import json
import glob
import httpx
import re
from agents.base import BaseAgent, Task, Result

class DeveloperAgent(BaseAgent):
    name = "Developer"
    display_name = "Software Developer"

    async def execute(self, task: Task) -> Result:
        os.makedirs("src", exist_ok=True)

        research_notes = ""
        if os.path.exists("src/research_notes.txt"):
            with open("src/research_notes.txt", "r", encoding="utf-8") as f:
                research_notes = f.read()

        print(f"[Developer] در حال بررسی پروژه برای تسک: {task.description}", flush=True)

        is_edit = "edit" in task.description.lower() or "update" in task.description.lower() or "add to" in task.description.lower()
        existing_code = ""
        project_dir = ""

        if is_edit:
            existing_dirs = [d for d in glob.glob("src/project_*") if os.path.isdir(d)]
            if existing_dirs:
                project_dir = sorted(existing_dirs)[-1]
                for f in glob.glob(f"{project_dir}/**/*.py", recursive=True):
                    with open(f, "r") as file:
                        existing_code += f"\n--- {os.path.basename(f)} ---\n{file.read()}\n"

        if not project_dir:
            max_idx = max([int(os.path.basename(d).replace("project_", "")) for d in glob.glob("src/project_*") if os.path.isdir(d)] + [0])
            project_dir = f"src/project_{max_idx + 1:04d}"
            os.makedirs(project_dir, exist_ok=True)

        if is_edit and existing_code:
            prompt = f"""You are an expert Python developer.
Here is the EXISTING code of the project:
{existing_code}

Your task is to UPDATE this code to include the following feature: {task.description}
CRITICAL RULES:
1. Output ONLY valid JSON exactly like this example: {{"files": [{{"name": "main.py", "content": "updated code here"}}]}}
2. Do NOT use markdown. Output ONLY the JSON.
3. Include the full updated code for every file you modify.
"""
        else:
            prompt = f"""You are an expert Python developer. Create a new multi-file project for: {task.description}
Use these research notes if helpful:
{research_notes[:1000]}

CRITICAL RULES:
1. Output ONLY valid JSON exactly like this example: {{"files": [{{"name": "main.py", "content": "code here"}}, {{"name": "utils.py", "content": "code here"}}]}}
2. Do NOT use markdown. Output ONLY the JSON.
3. Include full, working code in every file. You can create subfolders if needed (e.g., "templates/index.html").
"""

        raw = await self.call_self(prompt)
        
        # 🟢 اصلاح باگ JSON: پیدا کردن اولین { و آخرین }
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            clean = match.group(0)
            try:
                data = json.loads(clean)
                files = data.get("files", [])
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
                        
                print(f"[Developer] کدها با موفقیت در {project_dir} ذخیره شدند.", flush=True)
                self.log_event("code_generated", {"filename": f"{project_dir}/main.py", "code": final_main_code})
                return Result(task_id=task.id, success=True)
            except Exception as e:
                print(f"[Developer] خطا در پردازش JSON: {e}", flush=True)
                return Result(task_id=task.id, success=False, output=str(e))
        else:
            print(f"[Developer] خطا: هیچ ساختار JSON معتبری در پاسخ هوش مصنوعی یافت نشد.", flush=True)
            return Result(task_id=task.id, success=False, output="No JSON found")

    async def call_self(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:5001/v1/chat/completions",
                    json={
                        "model": "openai/gpt-oss-120b", 
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=120.0
                )
                data = resp.json()
                if 'choices' in data: 
                    return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"خطا در ارتباط با Smart Router: {e}", flush=True)
        return '{"files": [{"name": "main.py", "content": "print(\'Error generating code\')"}]}'
