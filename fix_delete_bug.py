import re

# ۱. بازنویسی بک‌اند برای اطمینان از وجود API حذف
web_ui_path = '/sdcard/omid-ai/web_ui.py'
with open(web_ui_path, 'r') as f: w = f.read()

# حذف API قدیمی اگر وجود دارد
w = re.sub(r'@app\.delete\("/api/files/\{filename:path\}"\).*?(?=@app\.|\Z)', '', w, flags=re.DOTALL)

# اضافه کردن API جدید و صحیح
delete_api = '''
@app.delete("/api/files/{filename:path}")
async def delete_project_file(filename: str) -> dict:
    file_path = os.path.join("src", filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
    return {"status": "error", "detail": "File not found"}

@app.get("/sse")'''

w = w.replace('@app.get("/sse")', delete_api)
with open(web_ui_path, 'w') as f: f.write(w)
print("✅ API حذف فایل در بک‌اند اصلاح شد.")

# ۲. اصلاح فرانت‌اند
html_path = '/sdcard/omid-ai/index.html'
with open(html_path, 'r') as f: h = f.read()

# الف) کوچیک‌تر کردن کادر Select (کادر بسته)
h = re.sub(
    r'<select id="fileSelect"[^>]*>',
    '<select id="fileSelect" onchange="loadFile()" class="bg-gray-900 text-[10px] text-gray-300 rounded px-1 py-1 border border-gray-600 w-[80px] md:w-[130px] truncate">',
    h
)

# ب) اصلاح تابع حذف برای نمایش درست خطا
old_delete_js = """if(data.status === 'success') { 
                        clearCode();
                        fetchFiles(); 
                    } else { 
                        alert('Error: ' + data.message); 
                    }"""

new_delete_js = """if(data.status === 'success') { 
                        clearCode();
                        fetchFiles(); 
                    } else { 
                        alert('Error: ' + (data.detail || data.message || 'Unknown error')); 
                    }"""

if old_delete_js in h:
    h = h.replace(old_delete_js, new_delete_js)
    print("✅ پیام خطای حذف فایل در فرانت‌اند اصلاح شد.")
else:
    # اگر فاصله‌ها تغییر کرده بود، با Regex جایگزین میکنیم
    h = re.sub(r"alert\('Error: ' \+ data\.message\);", "alert('Error: ' + (data.detail || data.message || 'Unknown error'));", h)
    print("✅ پیام خطا (روش دوم) اصلاح شد.")

with open(html_path, 'w') as f: f.write(h)
print("✅ سایز منوی Select کوچک شد.")
