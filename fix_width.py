import re

p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# تغییر نسبت گرید به 2fr برای کد و 1fr برای لاگ‌ها
old_grid = '<div class="grid grid-cols-2 gap-2 md:gap-4 h-[calc(100vh-290px)]">'
new_grid = '<div class="grid grid-cols-[2fr_1fr] gap-1 md:gap-4 h-[calc(100vh-290px)]">'

if old_grid in h:
    h = h.replace(old_grid, new_grid)
    print("✅ چیدمان به نسبت ۲ به ۱ تغییر یافت (کد بزرگتر شد).")
else:
    # اگر ساختار کمی تغییر کرده بود، با Regex جایگزین می‌کنیم
    h = re.sub(r'<div class="grid grid-cols-2.*?h-\[\d+px\]">', new_grid, h)
    print("✅ چیدمان (با روش جایگزین) به نسبت ۲ به ۱ تغییر یافت.")

# جلوگیری از بیرون زدن متن‌های طولانی در لاگ‌ها
if 'id="logContainer"' in h and 'break-words' not in h:
    h = h.replace('id="logContainer" class="flex-1 p-2 md:p-3 overflow-y-auto', 'id="logContainer" class="flex-1 p-2 md:p-3 overflow-y-auto break-words')

with open(p, 'w') as f: f.write(h)
print("✅ فایل index.html با موفقیت آپدیت شد.")
