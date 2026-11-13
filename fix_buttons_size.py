import re

p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. بزرگتر کردن منوی انتخاب فایل در رایانه (md:text-sm و md:w-[180px])
h = re.sub(
    r'<select id="fileSelect"[^>]*>',
    '<select id="fileSelect" onchange="loadFile()" class="bg-gray-900 text-[10px] md:text-sm text-gray-300 rounded px-1 md:px-3 py-1 md:py-1.5 border border-gray-600 w-[80px] md:w-[180px] truncate">',
    h
)

# ۲. بزرگتر کردن تمام دکمه‌های کنار منو (Refresh, Delete, Clear, Copy, Save, ZIP)
# ما کلاس‌های مربوط به پدینگ و سایز فونت را در حالت md تغییر می‌دهیم
h = re.sub(
    r'class="([^"]*)text-\[10px\] md:text-xs px-2 py-1 rounded([^"]*)"',
    r'class="\1text-[10px] md:text-sm px-2 md:px-3 py-1 md:py-1.5 rounded\2"',
    h
)

with open(p, 'w') as f: f.write(h)
print("✅ سایز دکمه‌ها و منوی Select فقط در حالت رایانه بزرگ‌تر شد.")
