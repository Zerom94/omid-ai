import re

manager_path = '/sdcard/omid-ai/core/manager.py'
with open(manager_path, 'r') as f:
    code = f.read()

# جایگزینی جداکننده قدیمی با جداکننده هوشمند (فقط نقطه‌ای که بعدش فاصله است)
old_regex = r"lines = re\.split\(r'\[\.\\n\]\|\\bthen\\b', goal\)"
new_regex = r"lines = re.split(r'\\.\\s+|\\n|\\bthen\\b', goal)"

if "re.split(r'[.\\n]|\\bthen\\b', goal)" in code:
    code = code.replace("re.split(r'[.\\n]|\\bthen\\b', goal)", "re.split(r'\\.\\s+|\\n|\\bthen\\b', goal)")
    with open(manager_path, 'w') as f:
        f.write(code)
    print("✅ باگ جداکننده آدرس در manager.py با موفقیت رفع شد!")
else:
    print("⚠️ الگوی مورد نظر پیدا نشد. لطفاً دستی بررسی کنید.")
