import os
import re

agents_to_update = {
    "research_agent.py": "research",
    "analyst_agent.py": "analyst",
    "testing_agent.py": "testing",
    "automation_agent.py": "automation",
    "quality_control_agent.py": "quality_control",
    "memory_agent.py": "memory"
}

for filename, key in agents_to_update.items():
    path = f"/sdcard/omid-ai/agents/{filename}"
    if not os.path.exists(path):
        continue
        
    with open(path, "r") as f: code = f.read()
    
    # اگر از قبل آپدیت نشده باشد
    if "agents_knowledge.json" not in code:
        # پیدا کردن تابع execute
        match = re.search(r'(async def execute\(self, task: Task\) -> Result:\s*\n)', code)
        if match:
            injection = f'''        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        rules = ""
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                import json
                rules = json.load(f).get("{key}", "")
                if rules:
                    print(f"[{{self.name}}] 🎓 Using latest rules: {{rules}}", flush=True)
'''
            # تزریق کد خواندن دانش در ابتدای تابع
            code = code.replace(match.group(1), match.group(1) + injection)
            with open(path, "w") as f: f.write(code)
            print(f"✅ ایجنت {filename} مجهز به قوانین جدید شد.")
        else:
            print(f"⚠️ تابع execute در {filename} پیدا نشد.")
    else:
        print(f"ℹ️ ایجنت {filename} از قبل مجهز بود.")
