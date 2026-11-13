p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()
old = "addLog('> Mission Started', 'text-blue-400');"
new = "addLog('> Mission Started', 'text-blue-400');\n            document.getElementById('codeContent').innerText = '# Processing mission...';\n            const sel = document.getElementById('fileSelect');\n            if(sel) sel.value = '';"
if old in h and "Processing mission..." not in h:
    h = h.replace(old, new)
    with open(p, 'w') as f: f.write(h)
    print("✅ UI: صفحه کد هنگام شروع ماموریت پاک می‌شود.")
else:
    print("⚠️ از قبل اعمال شده یا پیدا نشد.")
