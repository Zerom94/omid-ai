import re

html_path = '/sdcard/omid-ai/index.html'
with open(html_path, 'r') as f:
    h = f.read()

# پیدا کردن بلوک کد قدیمی که با تمام شدن Manager، ماموریت را تمام شده فرض می‌کند
pattern = r"if\s*\(type\s*===\s*'complete'\s*&&\s*data\.agent\s*===\s*'Manager'\)\s*\{.*?fetchFiles\(.*?\);\s*\}"

new_js = """if (type === 'all_tasks_done') {
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('startBtn').innerText = 'Start';
                    addLog('> All Tasks Complete.', 'text-blue-400');
                    setLogsState('done');
                    setTimeout(() => fetchFiles(true), 1500);
                }"""

# جایگزینی با کد جدید
h = re.sub(pattern, new_js, h, flags=re.DOTALL)

# حذف خط لاگ قدیمی که زودتر از موعد چاپ می‌شد
h = h.replace("addLog('> Mission Complete.', 'text-blue-400');", "")

with open(html_path, 'w') as f:
    f.write(h)
print('✅ فایل index.html با موفقیت اصلاح شد!')
