p = '/sdcard/omid-ai/core/manager.py'
with open(p, 'r') as f: code = f.read()

old_block = '''            raw_web = await asyncio.to_thread(WebResearcher.search, topic)
            
            prompt = f"""
            You are an Elite AI Trainer. I have gathered this web text about the latest {agent} techniques:
            {raw_web[:1500]}
            
            Extract the top 3 actionable rules/techniques from this text that an AI {agent} agent should follow.
            Keep it short and highly technical (max 3 bullet points).
            Output ONLY plain text, no markdown.
            """'''

new_block = '''            raw_web = await asyncio.to_thread(WebResearcher.search, topic)
            print(f"[DEBUG] Web Search Result length: {len(raw_web)}", flush=True)
            
            prompt = f"""
            You are an Elite AI Trainer. Your job is to generate the top 3 highly technical rules for an AI agent of type '{agent}'.
            
            I searched the web for you. Here is the text (it might be empty or noisy):
            ---
            {raw_web[:1000]}
            ---
            
            INSTRUCTIONS:
            1. Extract rules from the text IF it contains valid information.
            2. If the text is empty, unhelpful, or contains an error, you MUST use your own internal expert knowledge to generate the top 3 best practices for a {agent} agent.
            3. Output ONLY the 3 rules as bullet points. Do NOT output markdown like ```json. Just plain text.
            """'''

if old_block in code:
    code = code.replace(old_block, new_block)
    with open(p, 'w') as f: f.write(code)
    print("✅ سیستم آموزش هوشمندتر شد (استفاده از دانش درونی در صورت خطای وب).")
else:
    print("⚠️ بلوک کد پیدا نشد. لطفاً دستی بررسی کنید.")
