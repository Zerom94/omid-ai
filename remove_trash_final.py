import re

p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. حذف دکمه HTML سطل زباله
h = re.sub(r'<button onclick="deleteFile\(\)".*?</button>', '', h, flags=re.DOTALL)

# ۲. حذف تابع جاوااسکریپت مربوط به سطل زباله
h = re.sub(r'function deleteFile\(\) \{.*?\}', '', h, flags=re.DOTALL)

# ۳. اصلاح فاصله‌ها (اگر فاصله اضافه‌ای ماند)
h = h.replace('<button onclick="clearCode()"', '\n<button onclick="clearCode()"')

with open(p, 'w') as f: f.write(h)
print("✅ دکمه سطل زباله و کدهای مربوط به آن برای همیشه حذف شدند.")
