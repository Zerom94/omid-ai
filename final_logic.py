import os

# ۱. اصلاح فایل web_ui.py
web_path = '/sdcard/omid-ai/web_ui.py'
with open(web_path, 'r') as f:
    w = f.read()

# جایگزینی کد قدیمی با کد جدید در پایتون
w = w.replace('broadcast("complete", {"agent": "Manager", "status": "Mission complete"})', 'broadcast("all_tasks_done", {"agent": "System", "status": "Complete"})')
w = w.replace("broadcast('complete', {'agent': 'Manager', 'status': 'Mission complete'})", 'broadcast("all_tasks_done", {"agent": "System", "status": "Complete"})')

with open(web_path, 'w') as f:
    f.write(w)
print("✅ فایل web_ui.py با موفقیت اصلاح شد.")

# ۲. اصلاح فایل index.html
html_path = '/sdcard/omid-ai/index.html'
with open(html_path, 'r') as f:
    h = f.read()

# جایگزینی شرط قدیمی با شرط جدید در جاوااسکریپت
h = h.replace("if (type === 'complete' && data.agent === 'Manager')", "if (type === 'all_tasks_done')")
h = h.replace('if (type === "complete" && data.agent === "Manager")', "if (type === 'all_tasks_done')")

# اطمینان از فعال بودن باز شدن خودکار فایل
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
print("✅ فایل index.html با موفقیت اصلاح شد.")
