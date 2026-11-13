p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. اطمینان از اینکه تابع با پارامتر True صدا زده می‌شود
h = h.replace('setTimeout(fetchFiles, 1000);', 'setTimeout(() => fetchFiles(true), 1500);')

# ۲. تزریق کد باز کردن خودکار فایل
auto_code = """
                    if (autoSelect && data.files.length > 0) {
                        let targetFile = data.files.find(f => f.endsWith('main.py')) || data.files[0];
                        select.value = targetFile;
                        loadFile();
                    }"""

if 'if (autoSelect && data.files.length > 0)' not in h:
    target = "addLog(`> Found ${data.files.length} file(s).`, 'text-green-400');"
    if target in h:
        h = h.replace(target, target + auto_code)

with open(p, 'w') as f: f.write(h)
print("✅ فایل index.html با موفقیت اصلاح شد.")
