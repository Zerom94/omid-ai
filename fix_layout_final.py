import re

p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. تنظیمات رایانه: نسبت ۳ به ۱ (کد پهن‌تر، لاگ باریک‌تر) و کشیدن تا انتهای صفحه
h = re.sub(
    r'(grid-cols-1\s+)(lg|md):grid-cols-\[.*?\]',
    r'\1md:grid-cols-[3fr_1fr]',
    h
)
# تغییر ارتفاع به dvh برای کشیده شدن تا پایین صفحه در رایانه
h = re.sub(
    r'(lg|md):h-\[calc\(100vh-\d+px\)\]',
    'md:h-[calc(100dvh-200px)]',
    h
)

# ۲. تنظیمات موبایل: کوچیک کردن آیکون‌ها و فونت‌ها
h = h.replace('text-lg md:text-2xl md:mb-1', 'text-sm md:text-2xl md:mb-1') # آیکون‌ها
h = h.replace('text-[8px] sm:text-[10px] md:text-sm', 'text-[7px] sm:text-[9px] md:text-sm') # نام ایجنت
h = h.replace('text-[7px] sm:text-[9px] md:text-xs', 'text-[6px] sm:text-[8px] md:text-xs') # وضعیت (Idle)

# آپدیت کردن کدهای جاوا اسکریپت که وضعیت‌ها رو تغییر میدن
h = h.replace("text-[7px] sm:text-[9px] md:text-xs text-purple-400", "text-[6px] sm:text-[8px] md:text-xs text-purple-400")
h = h.replace("text-[7px] sm:text-[9px] md:text-xs text-green-400", "text-[6px] sm:text-[8px] md:text-xs text-green-400")
h = h.replace("text-[7px] sm:text-[9px] md:text-xs text-red-400", "text-[6px] sm:text-[8px] md:text-xs text-red-400")

# ۳. اطمینان از اینکه باکس کد و لاگ در موبایل زیر هم و در رایانه کنار هم باشند
if 'grid grid-cols-1 md:grid-cols-[3fr_1fr]' not in h:
    # اگر کلاس پیدا نشد، به زور اضافه میکنیم
    h = h.replace('class="grid grid-cols-1', 'class="grid grid-cols-1 md:grid-cols-[3fr_1fr]')

with open(p, 'w') as f: f.write(h)
print("✅ چیدمان به درستی اصلاح شد (رایانه: کشیده تا پایین، موبایل: آیکون‌های کوچک‌تر).")
