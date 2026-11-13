p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. اضافه کردن متغیر global برای تشخیص آموزش
if 'let isTrainingMode = false;' not in h:
    h = h.replace('let eventSource = null;', 'let eventSource = null;\n        let isTrainingMode = false;')

# ۲. تنظیم متغیر در تابع startMission
if "isTrainingMode = goal" not in h:
    h = h.replace(
        "const goal = document.getElementById('missionInput').value.trim();",
        "const goal = document.getElementById('missionInput').value.trim();\n            isTrainingMode = goal.toLowerCase().startsWith('!train');"
    )

# ۳. جلوگیری از لود شدن کد قدیمی در پایان ماموریت
old_logic = "setTimeout(() => fetchFiles(true), 1000);"
new_logic = """if (isTrainingMode) {
                        document.getElementById('codeContent').innerText = '# Knowledge Base Updated Successfully. Check Terminal for details.';
                        const sel = document.getElementById('fileSelect');
                        if(sel) sel.value = '';
                    } else {
                        setTimeout(() => fetchFiles(true), 1000);
                    }"""

if old_logic in h and "Knowledge Base Updated Successfully" not in h:
    h = h.replace(old_logic, new_logic)
    with open(p, 'w') as f: f.write(h)
    print("✅ باگ نمایش کد در فرآیند آموزش (!train) برطرف شد.")
else:
    # روش جایگزین اگر ساختار عوض شده بود
    import re
    h = re.sub(r'setTimeout\(\(\) => fetchFiles\(true\), 1000\);', new_logic, h)
    with open(p, 'w') as f: f.write(h)
    print("✅ باگ نمایش کد (روش جایگزین) برطرف شد.")
