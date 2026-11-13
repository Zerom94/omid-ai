p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f: h = f.read()

# اصلاح انیمیشن برای اینکه هر ۳ چراغ با هم و به درستی چشمک بزنند
old_css = """@keyframes blink-yellow { 0%, 100% { background-color: #eab308; opacity: 1; } 50% { background-color: #eab308; opacity: 0.2; } }
        .blink-1 { animation: blink-yellow 1.5s infinite 0s; }
        .blink-2 { animation: blink-yellow 1.5s infinite 0.5s; }
        .blink-3 { animation: blink-yellow 1.5s infinite 1s; }"""

new_css = """@keyframes blink-yellow { 0%, 100% { background-color: #eab308; opacity: 1; box-shadow: 0 0 8px #eab308; } 50% { background-color: #eab308; opacity: 0.2; box-shadow: none; } }
        .blink-yellow { animation: blink-yellow 1s infinite; }"""

if old_css in h:
    h = h.replace(old_css, new_css)

h = h.replace("dot.classList.add(`blink-${index + 1}`)", "dot.classList.add('blink-yellow')")

with open(p, 'w') as f: f.write(h)
print("✅ انیمیشن چراغ‌های زرد اصلاح شد.")
