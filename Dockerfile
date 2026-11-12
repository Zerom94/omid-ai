# استفاده از پایتون 3.11 به عنوان پایه
FROM python:3.11-slim

# تنظیم پوشه کاری
WORKDIR /app

# کپی کردن فایل‌های نیازمندی و نصب آن‌ها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن تمام فایل‌های پروژه
COPY . .

# تنظیم متغیرهای محیطی (کلیدها از پنل سرور تنظیم می‌شوند)
ENV GROQ_API_KEY=""
ENV OPENROUTER_API_KEY=""

# اکسپوز کردن پورت وب‌سرور
EXPOSE 8000

# دستور اجرای همزمان روتر (5001) و وب‌سرور (8000)
CMD python3 smart_router.py & uvicorn web_ui:app --host 0.0.0.0 --port 8000
