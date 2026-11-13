import re

p = '/sdcard/omid-ai/core/manager.py'
with open(p, 'r') as f: code = f.read()

new_topics = """        topics = {
            "manager": "advanced AI multi-agent orchestration and LLM routing techniques",
            "research": "web scraping bypass cloudflare captcha solving techniques and OSINT",
            "developer": "python AI integration security tools exploit development scripts",
            "analyst": "AI data analysis threat intelligence and anomaly detection",
            "security": "advanced web exploitation WAF bypass sql injection xss captcha bypass",
            "recon": "advanced bug bounty reconnaissance active directory enumeration osint techniques",
            "testing": "automated security testing and AI fuzzing techniques",
            "automation": "AI workflow automation bypass rate limits and robotic process automation",
            "memory": "vector database RAG techniques for cybersecurity data",
            "quality_control": "static code analysis for finding zero-day vulnerabilities",
            "other": "latest trends in artificial intelligence and cybersecurity 2024"
        }"""

old_pattern = r"topics\s*=\s*\{.*?\}"
if re.search(old_pattern, code, flags=re.DOTALL):
    code = re.sub(old_pattern, new_topics, code, flags=re.DOTALL)
    with open(p, 'w') as f: f.write(code)
    print("✅ موضوعات آموزشی به هوش مصنوعی، امنیت، دور زدن و کپچا تغییر یافتند.")
else:
    print("⚠️ دیکشنری موضوعات پیدا نشد.")
