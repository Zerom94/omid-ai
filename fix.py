import re

# ۱. اصلاح web_ui.py (تغییر نام سیگنال پایان ماموریت)
web_path = '/sdcard/omid-ai/web_ui.py'
with open(web_path, 'r') as f:
    w = f.read()

old_broadcast = 'broadcast("complete", {"agent": "Manager", "status": "Mission complete"})'
new_broadcast = 'broadcast("all_tasks_done", {"agent": "System", "status": "Complete"})'

if old_broadcast in w:
    w = w.replace(old_broadcast, new_broadcast)
else:
    # اگر با کوتیشن تک نوشته شده بود
    old_b2 = "broadcast('complete', {'agent': 'Manager', 'status': 'Mission complete'})"
    w = w.replace(old_b2, new_broadcast)

with open(web_path, 'w') as f:
    f.write(w)
print('✅ فایل web_ui.py با موفقیت اصلاح شد.')

# ۲. اصلاح index.html (گوش دادن به سیگنال جدید و باز کردن خودکار فایل)
html_path = '/sdcard/omid-ai/index.html'
with open(html_path, 'r') as f:
    h = f.read()

# پیدا کردن بلوک کد قدیمی و جایگزینی آن
pattern = r"if\s*\(type\s*===\s*'complete'\s*&&\s*data\.agent\s*===\s*'Manager'\)\s*\{[^}]*setTimeout\([^)]*\);\s*\}"
new_js = """if (type === 'all_tasks_done') {
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('startBtn').innerText = 'Start';
                    addLog('> Mission Complete.', 'text-blue-400');
                    setLogsState('done');
                    setTimeout(() => fetchFiles(true), 1500);
                }"""

h = re.sub(pattern, new_js, h, flags=re.DOTALL)

# اطمینان از وجود پارامتر autoSelect
h = h.replace('function fetchFiles()', 'function fetchFiles(autoSelect = false)')

# تزریق منطق باز کردن خودکار
if 'if (autoSelect && data.files.length > 0)' not in h:
    target = "addLog(`> Found ${data.files.length} file(s).`, 'text-green-400');"
    inject = """addLog(`> Found ${data.files.length} file(s).`, 'text-green-400');
                    if (autoSelect && data.files.length > 0) {
                        let targetFile = data.files.find(f => f.endsWith('main.py')) || data.files[0];
                        select.value = targetFile;
                        loadFile();
                    }"""
    h = h.replace(target, inject)

with open(html_path, 'w') as f:
    f.write(h)
print('✅ فایل index.html با موفقیت اصلاح شد.')
