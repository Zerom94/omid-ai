import os

files_to_fix = [
    "/sdcard/omid-ai/agents/quality_control_agent.py",
    "/sdcard/omid-ai/agents/memory_agent.py"
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            code = f.read()
        
        if "import os" not in code:
            # اضافه کردن ایمپورت‌ها به بالای فایل
            code = "import os\nimport json\n" + code
            with open(file_path, "w") as f:
                f.write(code)
            print(f"✅ مشکل import در {os.path.basename(file_path)} برطرف شد.")
        else:
            print(f"ℹ️ {os.path.basename(file_path)} از قبل ایمپورت داشت.")
