p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. تشخیص حالت آموزش
if 'let isTrainingMode = false;' not in h:
    h = h.replace('let eventSource = null;', 'let eventSource = null;\n        let isTrainingMode = false;')

if "isTrainingMode = goal" not in h:
    h = h.replace(
        "const goal = document.getElementById('missionInput').value.trim();",
        "const goal = document.getElementById('missionInput').value.trim();\n            isTrainingMode = goal.toLowerCase().startsWith('!train');"
    )

# ۲. جلوگیری از لود کد قدیمی در پایان آموزش
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
    print("✅ باگ نمایش کد در حالت آموزش (!train) برطرف شد.")
else:
    import re
    h = re.sub(r'setTimeout\(\(\) => fetchFiles\(true\), 1000\);', new_logic, h)
    with open(p, 'w') as f: f.write(h)
    print("✅ باگ نمایش کد (روش جایگزین) برطرف شد.")
