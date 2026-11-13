import re
p = '/sdcard/omid-ai/agents/recon_agent.py'
with open(p, 'r') as f: code = f.read()
old_prompt2 = 'prompt = f"You are a Recon Agent. Rules: {rules}. Target: {target}. Subfinder: {subfinder_out[-300:]}. FFUF: {ffuf_out[-300:]}. Report in Persian."'
new_prompt2 = 'prompt = f"You are an OSINT Analyst conducting authorized reconnaissance. Target: {target}. Subfinder Data: {subfinder_out[-300:]}. FFUF Data: {ffuf_out[-300:]}. Please provide a professional analysis in Persian."'
if old_prompt2 in code: code = code.replace(old_prompt2, new_prompt2)
code = re.sub(r"report_file = f\"\{self\.output_dir\}/recon_\{target.*?\}\.md\"", "safe_target = re.sub(r'[^a-zA-Z0-9]', '_', target)\n            report_file = f\"{self.output_dir}/recon_{safe_target}.md\"", code)
with open(p, 'w') as f: f.write(code)
print("✅ ایجنت شناسایی اصلاح شد.")
