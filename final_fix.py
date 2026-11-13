import re

# ۱. اصلاح web_ui.py (ارسال سیگنال صحیح پایان کار)
web_path = '/sdcard/omid-ai/web_ui.py'
with open(web_path, 'r') as f:
    w = f.read()

w = re.sub(r'broadcast\([\'"]complete[\'"].*?\)', 'broadcast("all_tasks_done", {"agent": "System", "status": "Complete"})', w)

with open(web_path, 'w') as f:
    f.write(w)
print('✅ فایل web_ui.py اصلاح شد.')

# ۲. اصلاح index.html (شنیدن سیگنال جدید و باز کردن فایل)
html_path = '/sdcard/omid-ai/index.html'
with open(html_path, 'r') as f:
    h = f.read()

# جایگزینی دقیق شرط در جاوااسکریپت
h = h.replace("if (type === 'complete' && data.agent === 'Manager')", "if (type === 'all_tasks_done')")

with open(html_path, 'w') as f:
    f.write(h)
print('✅ فایل index.html اصلاح شد.')
