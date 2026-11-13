import os

files_to_fix = {
    "/sdcard/omid-ai/agents/recon_agent.py": "Recon",
    "/sdcard/omid-ai/agents/security_agent.py": "Security"
}

for file_path, agent_name in files_to_fix.items():
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            code = f.read()

        # اصلاح بلوک try/except در تابع analyze_with_ai
        # جایگزینی کد قدیمی با کدی که خطا را به درستی مدیریت می‌کند
        old_block = '''        try:
            res = requests.post(self.router_url, json=payload, timeout=120)
            ai_report = res.json()['choices'][0]['message']['content']'''
        
        new_block = '''        try:
            res = requests.post(self.router_url, json=payload, timeout=120)
            data = res.json()
            if 'choices' not in data:
                error_msg = f"AI API Error: {data.get('error', {}).get('message', 'Unknown error')}"
                print(f"[{agent_name}] ❌ {error_msg}", flush=True)
                return error_msg
            ai_report = data['choices'][0]['message']['content']'''

        # اگر بلوک قدیمی پیدا شد، جایگزین کن
        if old_block in code:
            code = code.replace(old_block, new_block)
            with open(file_path, "w") as f:
                f.write(code)
            print(f"✅ باگ KeyError در {agent_name} برطرف شد.")
        else:
            # روش جایگزین با Regex اگر فاصله‌ها تغییر کرده باشد
            import re
            code = re.sub(
                r"res = requests.post\(self.router_url, json=payload, timeout=120\)\s*ai_report = res.json\(\)\['choices'\]\[0\]\['message'\]\['content'\]",
                f"res = requests.post(self.router_url, json=payload, timeout=120)\n            data = res.json()\n            if 'choices' not in data:\n                error_msg = f\"AI API Error: {{data.get('error', {{}}).get('message', 'Unknown error')}}\"\n                print(f\"[{agent_name}] ❌ {{error_msg}}\", flush=True)\n                return error_msg\n            ai_report = data['choices'][0]['message']['content']",
                code
            )
            with open(file_path, "w") as f:
                f.write(code)
            print(f"✅ باگ KeyError در {agent_name} (روش جایگزین) برطرف شد.")
