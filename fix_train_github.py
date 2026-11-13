p = '/sdcard/omid-ai/core/manager.py'
with open(p, 'r') as f: code = f.read()

# تغییر موضوعات جستجو به سمت گیت‌هاب و سایت‌های فنی
old_topics = 'topics = {\n            "manager": "latest techniques for orchestrating multi-agent AI systems and LLM routing 2024",'
new_topics = 'topics = {\n            "manager": "github advanced multi-agent orchestration repository python",'

code = code.replace(old_topics, new_topics)
code = code.replace('"developer": "latest Python best practices and advanced coding techniques 2024"', '"developer": "github python advanced code architecture best practices"')
code = code.replace('"security": "latest web application penetration testing techniques OWASP 2024"', '"security": "github python security audit tools best practices"')
code = code.replace('"analyst": "latest techniques for data analysis, pandas, and generating insights with AI"', '"analyst": "github pandas advanced data analysis techniques"')

with open(p, 'w') as f: f.write(code)
print("✅ موضوعات آموزشی مدیر به سمت گیت‌هاب تغییر کرد.")
