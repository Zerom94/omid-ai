from agents.base import BaseAgent, Task, Result
import httpx
import os
from ddgs import DDGS
from bs4 import BeautifulSoup
import requests

class ResearchAgent(BaseAgent):
    name = "Research"
    display_name = "Web Researcher"

    async def execute(self, task: Task) -> Result:
        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        rules = ""
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                import json
                rules = json.load(f).get("research", "")
                if rules:
                    print(f"[{self.name}] 🎓 Using latest rules: {rules}", flush=True)
        print(f"🔍 [Research] در حال جستجو برای: {task.description}")
        
        # ۱. جستجو در DuckDuckGo
        search_results = []
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(task.description, max_results=3))
                search_results = results
        except Exception as e:
            print(f"⚠️ [Research] خطا در جستجو: {e}")
            return Result(task_id=task.id, success=True, output={"message": "Search failed."})

        if not search_results:
            return Result(task_id=task.id, success=True, output={"message": "No results found."})

        # ۲. استخراج متن از صفحات
        combined_text = ""
        for res in search_results:
            url = res.get('href')
            try:
                print(f"📄 [Research] در حال خواندن: {url}")
                page = requests.get(url, timeout=10)
                soup = BeautifulSoup(page.content, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text(separator=' ', strip=True)
                combined_text += f"\n\n--- Source: {url} ---\n{text[:3000]}\n"
            except Exception as e:
                print(f"⚠️ [Research] خطا در خواندن {url}: {e}")

        # ۳. خلاصه کردن با هوش مصنوعی
        prompt = f"""You are a research assistant. Summarize the following web content to help a developer write code for this task: "{task.description}"
Here is the content:
{combined_text}

Provide a concise, structured summary of the most important technical points, libraries, or code examples found.
"""
        
        summary = await self.llm_call(prompt)
        
        os.makedirs("src", exist_ok=True)
        with open("src/research_notes.txt", "w", encoding='utf-8') as f:
            f.write(f"Task: {task.description}\n\nSummary:\n{summary}")
            
        print(f"✅ [Research] تحقیق کامل شد و در src/research_notes.txt ذخیره شد.")
        
        return Result(task_id=task.id, success=True, output={"summary": summary})

    async def llm_call(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:5001/v1/chat/completions",
                    headers={},
                    json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]},
                    timeout=120.0
                )
                data = resp.json()
                if "choices" in data: return data["choices"][0]["message"]["content"]
        except Exception as e: 
            print(f"❌ [Research LLM] خطا: {e}")
        return "Could not summarize."
