import os
import json
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# 🔑 کلیدها
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") 
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") 

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    data = await request.json()
    prompt = data.get("messages", [{}])[-1].get("content", "")
    is_json = data.get("response_format", {}).get("type") == "json_object"
    
    if is_json:
        prompt += "\nOutput ONLY valid JSON. No markdown."

    # 🥇 لایه ۱: Groq (سریع‌ترین)
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": prompt}]
            }
            if is_json: payload["response_format"] = {"type": "json_object"}
                
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions", 
                                     headers=headers, json=payload, timeout=20.0)
            
            if resp.status_code == 200:
                print("[Router] ✅ Success via Groq")
                return JSONResponse(content=resp.json())
            else:
                print(f"[Router] ⚠️ Groq Error {resp.status_code}. Switching to GitHub...")
    except Exception as e:
        print(f"[Router] ⚠️ Groq Failed. Switching to GitHub...")

    # 🥈 لایه ۲: GitHub Models (پایدار)
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            if is_json: payload["response_format"] = {"type": "json_object"}
                
            resp = await client.post("https://models.inference.ai.azure.com/chat/completions", 
                                     headers=headers, json=payload, timeout=25.0)
            
            if resp.status_code == 200:
                print("[Router] ✅ Success via GitHub Models")
                return JSONResponse(content=resp.json())
            else:
                print(f"[Router] ⚠️ GitHub Error {resp.status_code}. Switching to Pollinations...")
    except Exception as e:
        print(f"[Router] ⚠️ GitHub Failed. Switching to Pollinations...")

    # 🥉 لایه ۳: Pollinations (بدون کلید - نجات‌دهنده نهایی)
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": "openai",
                "messages": [{"role": "user", "content": prompt}]
            }
            resp = await client.post("https://text.pollinations.ai/openai", 
                                     json=payload, timeout=40.0)
            
            if resp.status_code == 200:
                print("[Router] ✅ Success via Pollinations (No Key)")
                return JSONResponse(content=resp.json())
            else:
                print(f"[Router] ❌ Pollinations Error {resp.status_code}")
                return JSONResponse(status_code=500, content={"error": {"message": resp.text}})
                
    except Exception as e:
        print(f"[Router] ❌ Total failure: {e}")
        return JSONResponse(status_code=500, content={"error": {"message": str(e)}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
