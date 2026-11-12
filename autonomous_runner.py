import asyncio
import sys
import os
from core.manager import ManagerAgent
from core.memory import MemoryStore

async def main():
    if len(sys.argv) < 2:
        print("❌ لطفاً نام فایل متنی حاوی هدف را وارد کنید. مثال: python3 autonomous_runner.py goal.txt")
        return

    goal_file = sys.argv[1]
    if not os.path.exists(goal_file):
        print(f"❌ فایل {goal_file} پیدا نشد.")
        return

    with open(goal_file, 'r', encoding='utf-8') as f:
        goal = f.read().strip()

    print(f"🚀 شروع ماموریت خودمختار:\n{goal}\n")
    
    memory = MemoryStore()
    manager = ManagerAgent(config={}, memory=memory)
    
    # اجرای ماموریت بدون نیاز به مرورگر
    await manager.plan_and_dispatch(goal)
    
    print("\n✅ ماموریت خودمختار با موفقیت به پایان رسید! فایل‌ها در پوشه src ذخیره شدند.")

if __name__ == "__main__":
    asyncio.run(main())
