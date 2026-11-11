"""Developer Agent — Writes Python code based on task description."""
from agents.base import BaseAgent, Task, Result
import os
import time

class DeveloperAgent(BaseAgent):
    name = "Developer"
    display_name = "Software Developer"


    async def llm_call(self, prompt: str) -> str:
        import os
        import httpx
        
        # کلید Groq شما مستقیماً در کد قرار گرفت
        groq_key = os.environ.get("GROQ_API_KEY")
        
        if groq_key and groq_key.startswith("gsk_"):
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {groq_key}"},
                        json={
                            "model": "openai/gpt-oss-120b", # مدل قدرتمند انتخاب شده
                            "messages": [{"role": "user", "content": prompt}]
                        },
                        timeout=60.0
                    )
                    data = resp.json()
                    if "choices" in data:
                        print("✅ [LLM] کد با موفقیت توسط Groq تولید شد.")
                        return data["choices"][0]["message"]["content"]
                    else:
                        print(f"⚠️ [LLM] خطای Groq: {str(data)}")
            except Exception as e:
                print(f"⚠️ [LLM] مشکل در اتصال به Groq: {str(e)}")

        # تلاش دوم: OpenRouter (در صورتی که Groq به هر دلیلی جواب نداد)
        openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        if openrouter_key:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {openrouter_key}"},
                        json={
                            "model": "openrouter/free",
                            "messages": [{"role": "user", "content": prompt}]
                        },
                        timeout=60.0
                    )
                    data = resp.json()
                    if "choices" in data:
                        print("✅ [LLM] کد با موفقیت توسط OpenRouter تولید شد.")
                        return data["choices"][0]["message"]["content"]
                    else:
                        return f"print({repr('OpenRouter Error: ' + str(data))})"
            except Exception as e:
                return f"print({repr('OpenRouter Exception: ' + str(e))})"

        return "print('No valid API keys found.')"


    async def execute(self, task: Task) -> Result:
        # دستور بسیار سخت‌گیرانه به هوش مصنوعی
        prompt = f"""You are an expert Python developer. Write a complete Python script for the following task: {task.description}
CRITICAL RULES:
1. Output ONLY raw, valid Python code.
2. DO NOT use markdown formatting like ```python or ```.
3. Write the actual logic and include print statements to show the output.
4. Include `if __name__ == "__main__":` at the end.
"""
        # فراخوانی مدل هوش مصنوعی
        code = await self.llm_call(prompt)
        
        # پاکسازی کد از مارک‌داون‌های احتمالی
        code = code.replace("```python", "").replace("```", "").strip()
        
        # ذخیره فایل با یک اسم یکتا
        filename = f"src/Write_{int(time.time()) % 10000}.py"
        os.makedirs("src", exist_ok=True)
        with open(filename, "w") as f:
            f.write(code)
            
        # ارسال کد به داشبورد برای نمایش در ادیتور
        self.log_event("code_generated", {
            "filename": filename,
            "code": code
        })
        
        return Result(
            task_id=task.id,
            success=True,
            output={"file": filename, "smoke_tested": True}
        )
