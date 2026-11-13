p = '/sdcard/omid-ai/core/manager.py'
with open(p, 'r') as f: code = f.read()
old_if = 'if any(word in goal.lower() for word in ["upgrade", "train", "learn", "update yourself"]):'
new_if = 'if goal.startswith("!train") or "train all agents" in goal.lower():'
if old_if in code:
    code = code.replace(old_if, new_if)
    with open(p, 'w') as f: f.write(code)
    print("✅ دستور اختصاصی !train به مدیر اضافه شد.")
else:
    old_if2 = "if 'upgrade' in goal.lower() or 'train' in goal.lower() or 'update yourself' in goal.lower():"
    if old_if2 in code:
        code = code.replace(old_if2, new_if)
        with open(p, 'w') as f: f.write(code)
        print("✅ دستور اختصاصی !train (روش دوم) اضافه شد.")
    else:
        print("⚠️ شرط پیدا نشد.")
