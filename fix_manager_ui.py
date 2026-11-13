p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# پیدا کردن بلوک پایان کارها
target = "if (type === 'all_tasks_done') {"

# اضافه کردن کد برای سبز کردن چراغ مدیر
inject = """if (type === 'all_tasks_done') {
                    // سبز کردن چراغ مدیر در پایان کار
                    const mgrCard = document.getElementById('card-manager');
                    const mgrStatus = document.getElementById('status-manager');
                    if (mgrCard && mgrStatus) {
                        mgrCard.classList.remove('active');
                        mgrCard.classList.add('border-green-500');
                        mgrStatus.className = 'text-[7px] sm:text-[9px] md:text-xs text-green-400 font-bold mt-0.5 md:mt-1';
                        mgrStatus.innerText = 'Done';
                    }"""

if target in h and "سبز کردن چراغ مدیر" not in h:
    h = h.replace(target, inject)
    with open(p, 'w') as f: f.write(h)
    print("✅ باگ نمایش چراغ Manager در index.html برطرف شد.")
else:
    print("⚠️ بلوک پیدا نشد یا از قبل اصلاح شده است.")
