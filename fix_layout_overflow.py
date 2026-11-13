p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# ۱. شکستن خطوط طولانی در کد (اضافه کردن whitespace-pre-wrap و break-all)
h = h.replace(
    '<pre><code id="codeContent" class="text-xs md:text-sm text-gray-300 font-mono">',
    '<pre class="whitespace-pre-wrap break-all"><code id="codeContent" class="text-xs md:text-sm text-gray-300 font-mono">'
)

# ۲. جلوگیری از بیرون زدن باکس کد از گرید (اضافه کردن min-w-0 و overflow-hidden)
h = h.replace(
    '<div class="bg-gray-800 rounded-xl border border-gray-700 flex flex-col h-[400px] md:h-full">',
    '<div class="bg-gray-800 rounded-xl border border-gray-700 flex flex-col h-[400px] md:h-full min-w-0 overflow-hidden">'
)

# ۳. جلوگیری از بیرون زدن باکس لاگ‌ها
h = h.replace(
    '<div class="bg-gray-800 rounded-xl border border-gray-700 flex flex-col h-[400px] md:h-full">',
    '<div class="bg-gray-800 rounded-xl border border-gray-700 flex flex-col h-[400px] md:h-full min-w-0 overflow-hidden">'
)

with open(p, 'w') as f: f.write(h)
print("✅ باگ بیرون زدن کدهای طولانی (Overflow) برطرف شد.")
