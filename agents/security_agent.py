import subprocess
import os
import requests
import json
import re
import asyncio
from agents.base import BaseAgent, Task, Result

class GrayHatEngine:
    def __init__(self):
        self.output_dir = "/sdcard/omid-ai/security_scans"
        os.makedirs(self.output_dir, exist_ok=True)
        self.router_url = "http://127.0.0.1:5001/v1/chat/completions"
        self.nuclei_path = "/usr/local/bin/nuclei"
        self.nmap_path = "/usr/bin/nmap"

    def run_nmap(self, target):
        print(f"\n[Engine] 🔍 Running Nmap on {target}...", flush=True)
        cmd = [self.nmap_path, "-sT", "-sV", "-T4", "--top-ports", "100", target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.stdout
        except Exception as e:
            return f"Nmap failed: {str(e)}"

    def run_nuclei(self, target):
        print(f"[Engine] 🛡️ Running Nuclei on {target}...", flush=True)
        if not target.startswith("http"):
            target = "http://" + target
        output_file = f"{self.output_dir}/nuclei_{target.replace('http://', '').replace('https://', '').replace('/', '_')}.txt"
        cmd = [self.nuclei_path, "-u", target, "-severity", "critical,high", "-o", output_file, "-duc", "-timeout", "5", "-retries", "1", "-silent"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            return result.stdout
        except Exception as e:
            return f"Nuclei failed: {str(e)}"

    def run_sqlmap(self, target_url):
        print(f"[Engine] 💉 Running SQLMap on {target_url}...", flush=True)
        cmd = ["sqlmap", "-u", target_url, "--batch", "--level=1", "--risk=1", "--dbs", "--timeout=10", "--retries=1"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.stdout
        except Exception as e:
            return f"SQLMap failed: {str(e)}"

    def analyze_with_ai(self, target, nmap_out, nuclei_out, sqlmap_out):
        print(f"[Engine] 🧠 Analyzing results with AI (Groq)...", flush=True)
        prompt = f"""
        You are an expert Gray Hat Security Agent. I have scanned {target}.
        Results:
        --- NMAP ---
        {nmap_out[-500:] if nmap_out else 'No output'}
        --- NUCLEI ---
        {nuclei_out[-500:] if nuclei_out else 'No vulnerabilities'}
        --- SQLMAP ---
        {sqlmap_out[-500:] if sqlmap_out else 'No SQLi'}
        
        Provide a short technical report in Persian. Explain the vulnerabilities, exploit scenario, and patch.
        """
        payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
        try:
            response = requests.post(self.router_url, json=payload, timeout=120)
            data = response.json()
            if 'choices' in data:
                ai_report = data['choices'][0]['message']['content']
                report_file = f"{self.output_dir}/report_{target.replace('http://', '').replace('https://', '').replace('/', '_')}.md"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(ai_report)
                print(f"\n[Engine] ✅ Report saved to: {report_file}", flush=True)
                return ai_report
            return f"Router Error: {json.dumps(data)}"
        except Exception as e:
            return f"AI Connection Error: {str(e)}"

class SecurityAgent(BaseAgent):
    name = "Security"
    display_name = "Security"

    async def execute(self, task: Task) -> Result:
        print(f"\n>>> [SecurityAgent] Task received: {task.description}", flush=True)
        
        urls = re.findall(r'(https?://[^\s]+)', task.description)
        if urls:
            target = urls[0]
        else:
            target = task.description.strip().split()[-1]
            
        try:
            engine = GrayHatEngine()
            nmap_res = await asyncio.to_thread(engine.run_nmap, target)
            nuclei_res = await asyncio.to_thread(engine.run_nuclei, target)
            sqlmap_res = await asyncio.to_thread(engine.run_sqlmap, target)
            report = await asyncio.to_thread(engine.analyze_with_ai, target, nmap_res, nuclei_res, sqlmap_res)
            
            # ارسال گزارش به داشبورد برای نمایش در Modal
            self.log_event("report", {"agent": self.name, "content": report})
            
            print(f">>> [SecurityAgent] Scan complete!", flush=True)
            return Result(task_id=task.id, success=True, output=report)
        except Exception as e:
            print(f">>> [SecurityAgent] ERROR: {str(e)}", flush=True)
            return Result(task_id=task.id, success=False, output=str(e))
