import re

p = '/sdcard/omid-ai/core/manager.py'
with open(p, 'r') as f: code = f.read()

# تغییر موضوعات به مباحث پیشرفته‌تر
new_topics = """        topics = {
            "manager": "github advanced multi-agent orchestration frameworks langchain autogen",
            "research": "github advanced web scraping playwright selenium stealth",
            "developer": "github advanced python design patterns concurrency asyncio",
            "analyst": "github advanced data science machine learning scikit-learn",
            "security": "github advanced exploit development penetration testing tools",
            "recon": "github advanced osint tools subdomain enumeration",
            "testing": "github advanced python testing pytest coverage",
            "automation": "github advanced workflow automation apache airflow",
            "memory": "github advanced vector database chromadb pinecone",
            "quality_control": "github advanced static analysis pylint flake8",
            "other": "github advanced artificial intelligence agents"
        }"""

old_pattern = r"topics\s*=\s*\{.*?\}"
if re.search(old_pattern, code, flags=re.DOTALL):
    code = re.sub(old_pattern, new_topics, code, flags=re.DOTALL)
    with open(p, 'w') as f: f.write(code)
    print("✅ موضوعات آموزشی به مباحث پیشرفته‌تر (مثل LangChain و Playwright) تغییر یافت.")
else:
    print("⚠️ دیکشنری پیدا نشد.")
