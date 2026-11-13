import re

p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. موبایل: ۶ ستون (۲ ردیف) / رایانه: ۱ ردیف افقی
h = re.sub(
    r'<div class="grid grid-cols-[4-6][^>]*gap-[12][^>]*md:gap-[23][^>]*md:justify-between[^>]*">',
    '<div class="grid grid-cols-6 gap-1 md:flex md:flex-row md:flex-wrap lg:flex-nowrap md:gap-3 mb-4 w-full md:justify-between">',
    h
)

# ۲. آیکون‌ها: در موبایل ریز (۱۴px) / در رایانه بزرگ (2xl)
h = h.replace('<div class="text-lg md:text-2xl md:mb-1">', '<div class="text-[14px] md:text-2xl md:mb-1">')
h = h.replace('<div class="text-sm md:text-2xl md:mb-1">', '<div class="text-[14px] md:text-2xl md:mb-1">')

# ۳. نام ایجنت: در موبایل ریز / در رایانه بزرگ
h = h.replace('<div class="font-bold text-[8px] sm:text-[10px] md:text-sm text-center truncate w-full">', '<div class="font-bold text-[7px] md:text-sm text-center truncate w-full">')

# ۴. وضعیت (Idle): در موبایل ریز / در رایانه بزرگ
h = h.replace('class="text-[7px] sm:text-[9px] md:text-xs text-gray-500 mt-0.5 md:mt-1"', 'class="text-[6px] md:text-xs text-gray-500 mt-0.5 md:mt-1"')

# ۵. وضعیت در جاوااسکریپت (Working, Done, Failed) - هماهنگ با موبایل/رایانه
h = h.replace("status.className = 'text-[7px] sm:text-[9px] md:text-xs", "status.className = 'text-[6px] md:text-xs")
h = h.replace("el.className = 'text-[7px] sm:text-[9px] md:text-xs", "el.className = 'text-[6px] md:text-xs")

# ۶. رایانه: نسبت ۳ به ۱ (کد بزرگتر، لاگ باریک‌تر) و کشیدن تا انتهای صفحه
h = re.sub(
    r'class="grid grid-cols-1[^>]*gap-3 md:gap-4[^>]*"', 
    'class="grid grid-cols-1 md:grid-cols-[3fr_1fr] gap-3 md:gap-4 md:h-[calc(100dvh-180px)]"', 
    h
)

with open(p, 'w') as f: f.write(h)
print("✅ چیدمان کاملاً ایزوله شد (موبایل ۲ ردیف، رایانه بزرگ و کشیده تا پایین).")
