import os
import re

agents_to_fix = {
    "quality_control_agent.py": "quality_control",
    "memory_agent.py": "memory"
}

for filename, key in agents_to_fix.items():
    path = f"/sdcard/omid-ai/agents/{filename}"
    if not os.path.exists(path):
        print(f"فایل {filename} وجود ندارد.")
        continue
        
    with open(path, "r") as f: code = f.read()
    
    # جلوگیری از تزریق تکراری
    if "agents_knowledge.json" not in code:
        # پیدا کردن هر نوع تابع execute (چه async چه معمولی)
        match = re.search(r'(def execute\(self, task.*?\)[^:]*:\s*\n)', code)
        if match:
            injection = f'''        # خواندن دانش جدید
        import json
        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                rules = json.load(f).get("{key}", "")
                if rules:
                    print(f"[{{self.name}}] 🎓 Using latest rules: {{rules}}", flush=True)
'''
            code = code.replace(match.group(1), match.group(1) + injection)
            with open(path, "w") as f: f.write(code)
            print(f"✅ ایجنت {filename} با موفقیت تعمیر و مجهز شد.")
        else:
            print(f"⚠️ باز هم نتوانستم تابع execute را در {filename} پیدا کنم.")
    else:
        print(f"ℹ️ ایجنت {filename} از قبل مجهز بود.")
