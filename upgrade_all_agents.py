import re

p = '/sdcard/omid-ai/core/manager.py'
with open(p, 'r') as f: code = f.read()

# دیکشنری جدید شامل تمام ۱۱ ایجنت
new_topics = """        topics = {
            "manager": "latest techniques for orchestrating multi-agent AI systems and LLM routing 2024",
            "research": "latest techniques for AI web scraping, OSINT, and information retrieval",
            "developer": "latest Python best practices and advanced coding techniques 2024",
            "analyst": "latest techniques for data analysis, pandas, and generating insights with AI",
            "security": "latest web application penetration testing techniques OWASP 2024",
            "recon": "latest bug bounty reconnaissance techniques subdomain enumeration",
            "testing": "latest techniques for automated software testing, pytest, and AI code validation",
            "automation": "latest techniques for AI workflow automation and task scheduling",
            "memory": "latest techniques for RAG (Retrieval-Augmented Generation) and vector databases",
            "quality_control": "latest techniques for AI code review, linting, and static analysis",
            "other": "general AI best practices for specialized autonomous tasks"
        }"""

# پیدا کردن دیکشنری قدیمی و جایگزینی آن
old_pattern = r"topics\s*=\s*\{.*?\}"
if re.search(old_pattern, code, flags=re.DOTALL):
    code = re.sub(old_pattern, new_topics, code, flags=re.DOTALL)
    
    # آپدیت کردن قوانین پشتیبان (Fallback) برای همه ایجنت‌ها
    old_fallback = r"fallbacks\s*=\s*\{.*?\}"
    new_fallbacks = """fallbacks = {
                            "manager": "- Prioritize tasks logically.\\n- Ensure agents have clear instructions.",
                            "research": "- Use multiple search engines.\\n- Verify facts from reliable sources.",
                            "developer": "- Use type hints for all functions.\\n- Write modular code with docstrings.\\n- Handle exceptions gracefully.",
                            "analyst": "- Clean data before analysis.\\n- Visualize findings for better insights.",
                            "security": "- Always test for SQL Injection on all parameters.\\n- Check for Cross-Site Scripting (XSS).\\n- Scan for outdated server versions.",
                            "recon": "- Use subdomain enumeration to find hidden assets.\\n- Check for exposed .git and .env files.\\n- Look for directory listing vulnerabilities.",
                            "testing": "- Write unit tests for every critical path.\\n- Automate regression testing.",
                            "automation": "- Handle retries and timeouts.\\n- Log every automated action.",
                            "memory": "- Chunk large texts before embedding.\\n- Use cosine similarity for retrieval.",
                            "quality_control": "- Enforce PEP8 standards.\\n- Look for security vulnerabilities in code.",
                            "other": "- Always follow the principle of least privilege."
                        }"""
    code = re.sub(old_fallback, new_fallbacks, code, flags=re.DOTALL)
    
    with open(p, 'w') as f: f.write(code)
    print("✅ مدیر حالا برای تمام ۱۱ ایجنت آموزش می‌بیند!")
else:
    print("⚠️ دیکشنری پیدا نشد. لطفاً دستی بررسی کنید.")
