p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. دو ستونه کردن بخش کد و لاگ‌ها
h = h.replace('<div class="grid grid-cols-1 lg:grid-cols-2 gap-3 md:gap-4">', '<div class="grid grid-cols-2 gap-2 md:gap-4 h-[calc(100vh-290px)]">')

# ۲. تنظیم ارتفاع باکس‌ها برای پر کردن صفحه بدون اسکرول
h = h.replace('flex flex-col h-[280px] md:h-[450px]', 'flex flex-col h-full')

# ۳. کوچک‌تر کردن دکمه‌های Code Explorer تا در موبایل جا شوند
h = h.replace('text-[10px] md:text-xs px-2 py-1 rounded', 'text-[9px] md:text-xs px-1 py-1 rounded')
h = h.replace('gap-1 md:gap-2 items-center flex-wrap', 'gap-1 flex-wrap justify-center')

with open(p, 'w') as f: f.write(h)
print("✅ چیدمان داشبورد به حالت دو ستونه (بدون اسکرول) تغییر یافت.")
