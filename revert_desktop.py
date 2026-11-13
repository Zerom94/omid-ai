import re

p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. اصلاح باکس کد و لاگ‌ها (در موبایل زیر هم، در رایانه کد بزرگتر از لاگ)
# این الگو هر کلاسی که برای این بخش مانده را پیدا کرده و با کلاس صحیح جایگزین می‌کند
h = re.sub(
    r'<div class="grid[^>]*gap-3 md:gap-4[^>]*h-\[calc\(100vh-\d+px\)\]">',
    '<div class="grid grid-cols-1 md:grid-cols-[2fr_1fr] gap-3 md:gap-4 lg:h-[calc(100vh-280px)]">',
    h
)

# ۲. اصلاح ارتفاع کد و لاگ‌ها (در موبایل ۴۰۰ پیکسل، در رایانه پر کردن صفحه)
h = h.replace('flex flex-col h-[400px] lg:h-full', 'flex flex-col h-[400px] lg:h-full')

# ۳. اصلاح کارت‌های ایجنت‌ها (در موبایل ۴ ستونه، در رایانه ۱ ردیف افقی)
h = re.sub(
    r'<div class="grid[^>]*md:gap-3[^>]*md:justify-between[^>]*">',
    '<div class="grid grid-cols-4 sm:grid-cols-6 md:flex md:flex-row md:flex-wrap lg:flex-nowrap md:gap-2 mb-4 w-full md:justify-between gap-1">',
    h
)

# ۴. اصلاح باکس ورودی (در موبایل زیر هم، در رایانه کنار هم)
h = h.replace(
    'class="bg-gray-800 rounded-xl p-2 md:p-4 mb-3 flex flex-col sm:flex-row gap-2 border border-gray-700 shadow-lg"',
    'class="bg-gray-800 rounded-xl p-2 md:p-4 mb-3 flex flex-col md:flex-row gap-2 border border-gray-700 shadow-lg"'
)

with open(p, 'w') as f: f.write(h)
print("✅ چیدمان به حالت قبلی (کد بزرگتر در رایانه) بازگشت.")
