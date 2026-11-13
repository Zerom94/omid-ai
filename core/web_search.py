import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re
import random
import time

class WebResearcher:
    # لیست هویت‌های جعلی (مرورگرهای واقعی)
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
    ]

    @staticmethod
    def search(query: str, max_results: int = 3) -> str:
        print(f"[WebResearcher] 🕵️‍♂️ Human-like searching for: {query}", flush=True)
        try:
            # تاخیر تصادفی قبل از شروع جستجو (مثل تایپ کردن انسان)
            time.sleep(random.uniform(1.5, 4.0))

            # جستجو با تمرکز روی گیت‌هاب، استک‌اورفلو و مستندات فنی
            enhanced_query = f"{query} (site:owasp.org OR site:portswigger.net OR site:arxiv.org OR site:medium.com OR site:cloudflare.com OR site:hackerone.com OR site:github.com)"
            results = DDGS().text(enhanced_query, max_results=max_results)

            if not results:
                # اگر نتیجه‌ای پیدا نشد، جستجوی عادی
                results = DDGS().text(query, max_results=max_results)

            if not results:
                return "No results found."

            deep_content = ""
            for res in results:
                url = res.get('href', '')
                if not url.startswith('http'): continue

                print(f"[WebResearcher] 📖 Reading (human mode): {url[:50]}...", flush=True)

                # هدرهای کاملاً شبیه به مرورگر انسان
                headers = {
                    'User-Agent': random.choice(WebResearcher.USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }

                try:
                    # اگر لینک مربوط به فایل خام گیت‌هاب بود، مستقیماً متن کد را بگیر
                    if "raw.githubusercontent.com" in url:
                        text = requests.get(url, headers=headers, timeout=10).text
                        deep_content += f"\n--- Source (GitHub Raw Code): {url} ---\n{text[:2000]}...\n"
                    else:
                        # دریافت صفحه وب معمولی
                        response = requests.get(url, headers=headers, timeout=10)
                        
                        # اگر گیت‌هاب یا سایت ما را بلاک کرد (خطای 403)
                        if response.status_code == 403:
                            print("[WebResearcher] ⚠️ 403 Forbidden. Changing Identity and Retrying...", flush=True)
                            headers['User-Agent'] = random.choice(WebResearcher.USER_AGENTS)
                            time.sleep(random.uniform(2.0, 5.0))
                            response = requests.get(url, headers=headers, timeout=10)

                        soup = BeautifulSoup(response.text, 'html.parser')
                        for script in soup(["script", "style", "nav", "footer"]):
                            script.extract()

                        text = soup.get_text(separator=' ')
                        text = re.sub(r'\s+', ' ', text).strip()
                        deep_content += f"\n--- Source: {res.get('title')} ---\n{text[:2000]}...\n"
                except Exception as e:
                    print(f"[WebResearcher] ⚠️ Could not read {url}: {e}", flush=True)
                    deep_content += f"\n--- Snippet: {res.get('title')} ---\n{res.get('body', '')}\n"

                # تاخیر تصادفی بین خواندن هر مقاله (مثل انسان که بین مقالات سوییچ می‌کند)
                time.sleep(random.uniform(2.0, 5.0))

            return deep_content if deep_content else "Failed to extract deep content."
        except Exception as e:
            return f"Search failed: {str(e)}"
