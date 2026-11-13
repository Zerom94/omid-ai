p = '/sdcard/omid-ai/index.html'
with open(p, 'r') as f:
    h = f.read()

start = h.find("function fetchFiles")
end = h.find("function loadFile")

new_func = """function fetchFiles(autoSelect = false) {
            fetch('/api/files?t=' + new Date().getTime()).then(res => res.json()).then(data => {
                const select = document.getElementById('fileSelect');
                select.innerHTML = '<option value="">-- Select --</option>';
                if (data.files && data.files.length > 0) {
                    data.files.forEach(f => {
                        const opt = document.createElement('option');
                        opt.value = f;
                        opt.innerText = f;
                        select.appendChild(opt);
                    });
                    addLog('> Found ' + data.files.length + ' file(s).', 'text-green-400');
                    
                    if (autoSelect) {
                        let targetFile = data.files.find(f => f.endsWith('main.py')) || data.files[0];
                        select.value = targetFile;
                        loadFile();
                    }
                }
            }).catch(err => console.error("Error fetching files:", err));
        }

        """

if start != -1 and end != -1:
    h = h[:start] + new_func + h[end:]
    with open(p, 'w') as f:
        f.write(h)
    print("✅ تابع fetchFiles با موفقیت بازنویسی شد.")
else:
    print("⚠️ متاسفانه نتوانستم تابع را پیدا کنم.")
