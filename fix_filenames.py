import re

# اصلاح ایجنت Security
p1 = '/sdcard/omid-ai/agents/security_agent.py'
with open(p1, 'r') as f: code = f.read()
# اضافه کردن پاکسازی نام فایل
code = code.replace(
    "report_file = f\"{self.output_dir}/report_{target.replace('http://', '').replace('https://', '').replace('/', '_')}.md\"",
    "safe_target = re.sub(r'[^a-zA-Z0-9]', '_', target)\nreport_file = f\"{self.output_dir}/report_{safe_target}.md\""
)
with open(p1, 'w') as f: f.write(code)

# اصلاح ایجنت Recon
p2 = '/sdcard/omid-ai/agents/recon_agent.py'
with open(p2, 'r') as f: code = f.read()
code = code.replace(
    "report_file = f\"{self.output_dir}/recon_{target.replace('http://', '').replace('https://', '').replace('/', '_')}.md\"",
    "safe_target = re.sub(r'[^a-zA-Z0-9]', '_', target)\nreport_file = f\"{self.output_dir}/recon_{safe_target}.md\""
)
with open(p2, 'w') as f: f.write(code)

print("✅ باگ نام‌گذاری فایل‌ها در Security و Recon برطرف شد.")
