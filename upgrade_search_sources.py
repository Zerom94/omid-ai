p = '/sdcard/omid-ai/core/web_search.py'
with open(p, 'r') as f: code = f.read()

# تغییر کوئری جستجو برای شامل شدن سایت‌های معتبر
old_query = 'enhanced_query = f"{query} (site:github.com OR site:raw.githubusercontent.com OR site:stackoverflow.com)"'
new_query = 'enhanced_query = f"{query} (site:owasp.org OR site:portswigger.net OR site:arxiv.org OR site:medium.com OR site:cloudflare.com OR site:hackerone.com OR site:github.com)"'

if old_query in code:
    code = code.replace(old_query, new_query)
    with open(p, 'w') as f: f.write(code)
    print("✅ موتور جستجو ارتقا یافت (سایت‌های معتبر امنیتی و هوش مصنوعی اضافه شدند).")
else:
    print("⚠️ الگوی جستجو پیدا نشد. لطفاً فایل را چک کنید.")
