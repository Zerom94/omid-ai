import os
import httpx
import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/v1/messages")
async def anthropic_messages(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    model_name = data.get("model", "claude-3-5-sonnet-20241022")

    # تبدیل زبان Anthropic به OpenAI (برای Groq)
    openai_messages = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list): # اگر محتوا لیستی از بلوک‌ها بود
            text_content = "".join([c.get("text", "") for c in content if c.get("type") == "text"])
        else:
            text_content = content
        openai_messages.append({"role": msg.get("role"), "content": text_content})

    # ۱. ارسال درخواست به Groq
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json={"model": "openai/gpt-oss-120b", "messages": openai_messages},
                    timeout=120.0
                )
                
                if resp.status_code == 200:
                    print("✅ [Router] استفاده از Groq موفقیت‌آمیز بود.")
                    groq_data = resp.json()
                    reply_text = groq_data["choices"][0]["message"]["content"]
                    
                    # تبدیل جواب Groq به زبان Anthropic (برای کلود کد)
                    anthropic_response = {
                        "id": f"msg_{int(time.time())}",
                        "type": "message",
                        "role": "assistant",
                        "model": model_name,  # 🔥 ترفند: همان مدلی که کلود خواسته را برمی‌گردانیم
                        "content": [{"type": "text", "text": reply_text}],
                        "stop_reason": "end_turn",
                        "stop_sequence": None,
                        "usage": {"input_tokens": 10, "output_tokens": 10}
                    }
                    return JSONResponse(content=anthropic_response)
                else:
                    print(f"⚠️ [Router] خطای Groq: {resp.status_code}")
        except Exception as e:
            print(f"⚠️ [Router] خطای اتصال: {e}")

    return JSONResponse(status_code=500, content={"error": "Groq failed"})

# پشتیبانی از API استاندارد OpenAI (برای اطمینان)
@app.post("/v1/chat/completions")
async def openai_chat(request: Request):
    data = await request.json()
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}"},
                    json={"model": "openai/gpt-oss-120b", "messages": data.get("messages", [])},
                    timeout=120.0
                )
                return JSONResponse(content=resp.json())
        except Exception as e:
            pass
    return JSONResponse(status_code=500, content={"error": "Groq failed"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
