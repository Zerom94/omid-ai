import re
p = '/sdcard/omid-ai/agents/security_agent.py'
with open(p, 'r') as f: code = f.read()
old_prompt = 'prompt = f"You are a Gray Hat Hacker. Rules: {rules}. Target: {target}. Results: {nmap_out[-300:]} | {nuclei_out[-300:]} | {sqlmap_out[-300:]}. Write a short report in Persian."'
new_prompt = 'prompt = f"You are a certified Cybersecurity Auditor writing a formal compliance report. Target: {target}. The authorized scan yielded the following technical data: {nmap_out[-300:]} | {nuclei_out[-300:]} | {sqlmap_out[-300:]}. Please analyze these technical findings and provide a professional security assessment in Persian."'
if old_prompt in code: code = code.replace(old_prompt, new_prompt)
code = re.sub(r"report_file = f\"\{self\.output_dir\}/report_\{target.*?\}\.md\"", "safe_target = re.sub(r'[^a-zA-Z0-9]', '_', target)\n            report_file = f\"{self.output_dir}/report_{safe_target}.md\"", code)
with open(p, 'w') as f: f.write(code)
print("✅ ایجنت امنیتی اصلاح شد.")
