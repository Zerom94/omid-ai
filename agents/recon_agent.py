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
        cmd = [self.subfinder_path, "-d", domain, "-silent"]
        try: return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
        except Exception as e: return f"Failed: {str(e)}"

    def run_ffuf(self, target_url):
        cmd = [self.ffuf_path, "-u", f"{target_url}/FUZZ", "-w", self.wordlist, "-mc", "200,204,301,302,307,401,403", "-s"]
        try: return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
        except Exception as e: return f"Failed: {str(e)}"

    def analyze_with_ai(self, target, subfinder_out, ffuf_out, rules):
        prompt = f"You are an OSINT Analyst conducting authorized reconnaissance. Target: {target}. Subfinder Data: {subfinder_out[-300:]}. FFUF Data: {ffuf_out[-300:]}. Please provide a professional analysis in Persian."
        payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}
        try:
            res = requests.post(self.router_url, json=payload, timeout=120)
            data = res.json()
            if 'choices' not in data:
                error_msg = f"AI API Error: {data.get('error', {}).get('message', 'Unknown error')}"
                print(f"[{agent_name}] ❌ {error_msg}", flush=True)
                return error_msg
            ai_report = data['choices'][0]['message']['content']
            safe_target = re.sub(r'[^a-zA-Z0-9]', '_', target)
            report_file = f"{self.output_dir}/recon_{safe_target}.md"
            with open(report_file, 'w', encoding='utf-8') as f: f.write(ai_report)
            return ai_report
        except Exception as e: return str(e)

class ReconAgent(BaseAgent):
    name = "Recon"
    display_name = "Recon"

    async def execute(self, task: Task) -> Result:
        urls = re.findall(r'(https?://[^\s]+)', task.description)
        target_url = urls[0] if urls else "http://example.com"
        domain = target_url.replace("http://", "").replace("https://", "").split("/")[0]

        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        rules = ""
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f: rules = json.load(f).get("recon", "")

        try:
            engine = ReconEngine()
            subfinder_res = await asyncio.to_thread(engine.run_subfinder, domain)
            ffuf_res = await asyncio.to_thread(engine.run_ffuf, target_url)
            report = await asyncio.to_thread(engine.analyze_with_ai, target_url, subfinder_res, ffuf_res, rules)
            self.log_event("report", {"agent": self.name, "content": report})
            return Result(task_id=task.id, success=True, output=report)
        except Exception as e: return Result(task_id=task.id, success=False, output=str(e))
