import re

# ۱. حذف تاخیر از SQLMap (چون باعث کندی بیش از حد شده)
p1 = '/sdcard/omid-ai/agents/security_agent.py'
with open(p1, 'r') as f: code = f.read()
code = code.replace('"--random-agent", "--delay=2"]', '"--random-agent"]')
with open(p1, 'w') as f: f.write(code)
print("✅ تاخیر اضافی از ایجنت امنیتی برداشته شد.")

# ۲. اصلاح باگ جاوااسکریپت در index.html
p2 = '/sdcard/omid-ai/index.html'
with open(p2, 'r') as f: h = f.read()

# حذف کدی که باعث کرش می‌شود (اشاره به dropdownText)
bad_js = "\n            document.getElementById('codeContent').innerText = '# Processing mission...';\n            document.getElementById('dropdownText').innerText = '-- Select --';"
good_js = "\n            document.getElementById('codeContent').innerText = '# Processing mission...';\n            const fileSelect = document.getElementById('fileSelect');\n            if(fileSelect) fileSelect.value = '';"

if bad_js in h:
    h = h.replace(bad_js, good_js)
    with open(p2, 'w') as f: f.write(h)
    print("✅ باگ جاوااسکریپت (فریز شدن صفحه) برطرف شد.")
else:
    # روش جایگزین اگر فاصله‌ها فرق داشت
    h = re.sub(r"document\.getElementById\('codeContent'\)\.innerText = '# Processing mission\.\.\.';.*?document\.getElementById\('dropdownText'\)\.innerText = '-- Select --';", 
               "document.getElementById('codeContent').innerText = '# Processing mission...';", h, flags=re.DOTALL)
    with open(p2, 'w') as f: f.write(h)
    print("✅ باگ جاوااسکریپت (روش دوم) برطرف شد.")
