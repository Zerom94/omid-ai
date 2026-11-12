from agents.base import BaseAgent, Task, Result
import os, glob, json
import httpx

class DeveloperAgent(BaseAgent):
    name = "Developer"
    display_name = "Software Developer"

    async def execute(self, task: Task) -> Result:
        # پرامپت فوق سخت‌گیرانه: مجبور کردن هوش مصنوعی به ساخت همه فایل‌ها
        prompt = f"""You are an expert Python developer. 
Your task: {task.description}
CRITICAL RULES:
1. You MUST generate EVERY SINGLE FILE requested in the task. If the task asks for `main.py` and `utils.py`, your JSON MUST contain TWO entries in the "files" array.
2. DO NOT skip `utils.py`. DO NOT merge the code into `main.py`.
3. Output ONLY valid JSON exactly like this example:
{{"files": [{{"name": "utils.py", "content": "def multiply(a,b): return a*b"}}, {{"name": "main.py", "content": "from utils import multiply\\nprint('Welcome')"}}]}}
4. Include full, working code in every file.
"""
        os.makedirs("src", exist_ok=True)
        
        # اصلاح باگ: فقط پوشه‌ها را برای شماره‌گذاری در نظر بگیر، فایل‌های ZIP را نادیده بگیر
        existing_dirs = [d for d in glob.glob("src/project_*") if os.path.isdir(d)]
        max_idx = 0
        for d in existing_dirs:
            try:
                idx = int(os.path.basename(d).replace("project_", ""))
                if idx > max_idx: max_idx = idx
            except: 
                pass
        
        project_dir = f"src/project_{max_idx + 1:04d}"
        os.makedirs(project_dir, exist_ok=True)
        
        final_main_code = "# No code generated."
        raw = await self.llm_call(prompt)
        clean = raw.replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(clean)
            files = data.get("files", [])
            
            if len(files) < 2:
                print(f"⚠️ [Developer] هشدار: هوش مصنوعی فقط {len(files)} فایل ساخت، در حالی که باید بیشتر باشد.")
                
            for f in files:
                fname = f.get("name", "main.py")
                fcontent = f.get("content", "")
                with open(os.path.join(project_dir, fname), "w") as file:
                    file.write(fcontent)
                if fname == "main.py": final_main_code = fcontent
                
        except Exception as e:
            print(f"❌ [Developer] خطا در خواندن JSON: {e}")
            
        self.log_event("code_generated", {"filename": f"{project_dir}/main.py", "code": final_main_code})
        return Result(task_id=task.id, success=True)

    async def llm_call(self, prompt: str) -> str:
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {groq_key}"},
                        json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}},
                        timeout=60.0
                    )
                    data = resp.json()
                    if "choices" in data: return data["choices"][0]["message"]["content"]
            except Exception as e: 
                print(f"❌ [LLM] خطا در اتصال: {e}")
        return '{"files": [{"name": "main.py", "content": "print(1)"}]}'
