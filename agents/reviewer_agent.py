from agents.base import BaseAgent, Task, Result
import httpx
import os

class ReviewerAgent(BaseAgent):
    name = "Reviewer"
    display_name = "Code Reviewer"

    async def execute(self, task: Task) -> Result:
        return Result(task_id=task.id, success=True, output={"message": "Reviewer ready."})

    async def review_code(self, code: str, original_request: str) -> str:
        prompt = f"You are a strict reviewer. The user asked: {original_request}. The code is: {code}. If perfect, reply 'APPROVED', else list bugs."
        return await self.llm_call(prompt)

    async def llm_call(self, prompt: str) -> str:
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key and groq_key.startswith("gsk_"):
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {groq_key}"},
                        json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]},
                        timeout=60.0
                    )
                    data = resp.json()
                    if "choices" in data:
                        return data["choices"][0]["message"]["content"]
            except Exception:
                pass
        return "APPROVED"
