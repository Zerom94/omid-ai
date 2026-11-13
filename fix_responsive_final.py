p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. اصلاح چیدمان کد و لاگ‌ها (در موبایل زیر هم، در دسکتاپ ۲ به ۱)
h = h.replace(
    '<div class="grid grid-cols-[2fr_1fr] gap-1 md:gap-4 h-[calc(100vh-290px)]">',
    '<div class="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-3 md:gap-4 lg:h-[calc(100vh-250px)]">'
)

# ۲. اصلاح ارتفاع باکس‌ها (در موبایل ارتفاع ثابت کمتر، در دسکتاپ پر کردن صفحه)
h = h.replace('flex flex-col h-full', 'flex flex-col h-[300px] lg:h-full')

# ۳. اصلاح باکس ورودی (در موبایل زیر هم، در دسکتاپ کنار هم)
h = h.replace(
    'class="bg-gray-800 rounded-xl p-2 md:p-4 mb-3 flex flex-col md:flex-row gap-2 border border-gray-700 shadow-lg"',
    'class="bg-gray-800 rounded-xl p-2 md:p-4 mb-3 flex flex-col sm:flex-row gap-2 border border-gray-700 shadow-lg"'
)

# ۴. اصلاح کارت‌های ایجنت (در موبایل ۳ ستونه، در دسکتاپ یک ردیف کامل)
h = h.replace(
    '<div class="grid grid-cols-6 gap-1 md:flex md:flex-row md:flex-wrap lg:flex-nowrap md:gap-3 mb-4 w-full md:justify-between">',
    '<div class="grid grid-cols-3 sm:grid-cols-4 md:flex md:flex-row md:flex-wrap lg:flex-nowrap md:gap-3 mb-4 w-full md:justify-between gap-2">'
)

# ۵. اصلاح ارتفاع باکس‌های کد و لاگ در موبایل (کمی بلندتر از ۳۰۰)
h = h.replace('flex flex-col h-[300px] lg:h-full', 'flex flex-col h-[400px] lg:h-full')

with open(p, 'w') as f: f.write(h)
print("✅ چیدمان به صورت کامل برای موبایل و دسکتاپ اصلاح شد.")
