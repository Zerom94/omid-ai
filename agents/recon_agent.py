import subprocess
import os
import requests
import json
import re
import asyncio
from agents.base import BaseAgent, Task, Result

class ReconEngine:
    def __init__(self):
        self.output_dir = "/sdcard/omid-ai/security_scans"
        os.makedirs(self.output_dir, exist_ok=True)
        self.router_url = "http://127.0.0.1:5001/v1/chat/completions"
        self.subfinder_path = "/usr/local/bin/subfinder"
        self.ffuf_path = "/usr/local/bin/ffuf"
        self.wordlist = "/sdcard/omid-ai/wordlist.txt"

    def run_subfinder(self, domain):
        print(f"[ReconEngine] 🛰️ Running Subfinder on {domain}...", flush=True)
        cmd = [self.subfinder_path, "-d", domain, "-silent"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.stdout
        except Exception as e:
            return f"Subfinder failed: {str(e)}"

    def run_ffuf(self, target_url):
        print(f"[ReconEngine] 📂 Running FFUF on {target_url}...", flush=True)
        # فقط برای تست، تعداد درخواست‌ها را محدود می‌کنیم تا سرور هدف بلاک نشود
        cmd = [self.ffuf_path, "-u", f"{target_url}/FUZZ", "-w", self.wordlist, "-mc", "200,204,301,302,307,401,403", "-s"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return result.stdout
        except Exception as e:
            return f"FFUF failed: {str(e)}"

    def analyze_with_ai(self, target, subfinder_out, ffuf_out):
        print(f"[ReconEngine] 🧠 Analyzing Recon results with AI (Groq)...", flush=True)
        prompt = f"""
        You are an expert OSINT and Recon Agent. I have scanned {target}.
        Results:
        --- SUBFINDER (Subdomains) ---
        {subfinder_out[-800:] if subfinder_out else 'No subdomains found'}
        --- FFUF (Hidden Directories) ---
        {ffuf_out[-800:] if ffuf_out else 'No hidden directories found'}
        
        Provide a short technical report in Persian. Explain what these subdomains and directories mean, 
        possible security risks (like exposed admin panels or backup files), and recommendations.
        """
        payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
        try:
            response = requests.post(self.router_url, json=payload, timeout=120)
            data = response.json()
            if 'choices' in data:
                ai_report = data['choices'][0]['message']['content']
                report_file = f"{self.output_dir}/recon_{target.replace('http://', '').replace('https://', '').replace('/', '_')}.md"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(ai_report)
                return ai_report
            return f"Router Error: {json.dumps(data)}"
        except Exception as e:
            return f"AI Connection Error: {str(e)}"

class ReconAgent(BaseAgent):
    name = "Recon"
    display_name = "Recon"

    async def execute(self, task: Task) -> Result:
        print(f"\n>>> [ReconAgent] Task received: {task.description}", flush=True)
        
        # استخراج دامنه از متن
        urls = re.findall(r'(https?://[^\s]+)', task.description)
        if urls:
            target_url = urls[0]
        else:
            # اگر کاربر لینک نداد، خودش لینک می‌سازد
            domain_match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', task.description)
            domain = domain_match.group(1) if domain_match else "example.com"
            target_url = f"http://{domain}"
            
        # جدا کردن دامنه خالص برای Subfinder
        domain = target_url.replace("http://", "").replace("https://", "").split("/")[0]
        print(f">>> [ReconAgent] Target domain: {domain} | URL: {target_url}", flush=True)

        try:
            engine = ReconEngine()
            subfinder_res = await asyncio.to_thread(engine.run_subfinder, domain)
            ffuf_res = await asyncio.to_thread(engine.run_ffuf, target_url)
            report = await asyncio.to_thread(engine.analyze_with_ai, target_url, subfinder_res, ffuf_res)
            
            # ارسال گزارش به داشبورد
            self.log_event("report", {"agent": self.name, "content": report})
            
            print(f">>> [ReconAgent] Scan complete!", flush=True)
            return Result(task_id=task.id, success=True, output=report)
        except Exception as e:
            print(f">>> [ReconAgent] ERROR: {str(e)}", flush=True)
            return Result(task_id=task.id, success=False, output=str(e))
