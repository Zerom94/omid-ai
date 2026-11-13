import re

# ۱. اضافه کردن API حذف فایل به web_ui.py
web_ui_path = '/sdcard/omid-ai/web_ui.py'
with open(web_ui_path, 'r') as f: w = f.read()

if '@app.delete("/api/files/{filename:path}")' not in w:
    delete_api = '''
@app.delete("/api/files/{filename:path}")
async def delete_project_file(filename: str) -> dict:
    safe_name = os.path.basename(filename)
    file_path = os.path.join("src", filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    return {"status": "error", "message": "File not found"}

@app.get("/sse")'''
    w = w.replace('@app.get("/sse")', delete_api)
    with open(web_ui_path, 'w') as f: f.write(w)
    print("✅ API حذف فایل به بک‌اند اضافه شد.")

# ۲. تغییرات فرانت‌اند (index.html)
html_path = '/sdcard/omid-ai/index.html'
with open(html_path, 'r') as f: h = f.read()

# الف) کوچیک کردن منوی Select
h = re.sub(
    r'<select id="fileSelect"[^>]*>',
    '<select id="fileSelect" onchange="loadFile()" class="bg-gray-900 text-[10px] md:text-xs text-gray-300 rounded px-1 md:px-2 py-1 border border-gray-600 w-[110px] md:w-[160px] truncate">',
    h
)

# ب) اضافه کردن دکمه سطل زباله کنار دکمه رفرش
if 'onclick="deleteFile()"' not in h:
    h = h.replace(
        '<button onclick="fetchFiles()" class="bg-blue-600 hover:bg-blue-700 text-white text-[10px] md:text-xs px-2 py-1 rounded">🔄</button>',
        '<button onclick="fetchFiles()" class="bg-blue-600 hover:bg-blue-700 text-white text-[10px] md:text-xs px-2 py-1 rounded" title="Refresh">🔄</button>\n                        <button onclick="deleteFile()" class="bg-red-700 hover:bg-red-800 text-white text-[10px] md:text-xs px-2 py-1 rounded" title="Delete File">🗑️</button>'
    )

# ج) اضافه کردن تابع JavaScript برای حذف فایل
if "function deleteFile()" not in h:
    delete_js = """
        function deleteFile() {
            const file = document.getElementById('fileSelect').value;
            if (!file) return alert('Please select a file to delete first.');
            if (!confirm(`Are you sure you want to delete ${file}?`)) return;
            
            fetch(`/api/files/${file}`, { method: 'DELETE' })
                .then(res => res.json())
                .then(data => {
                    if(data.status === 'success') { 
                        clearCode();
                        fetchFiles(); 
                    } else { 
                        alert('Error: ' + data.message); 
                    }
                });
        }
        function fetchFiles("""
    # جایگزینی دقیق برای قرار دادن تابع درست قبل از fetchFiles
    h = h.replace("function fetchFiles(", delete_js)

with open(html_path, 'w') as f: f.write(h)
print("✅ سایز منوی Select کوچک شد و دکمه حذف 🗑️ به فرانت‌اند اضافه شد.")
