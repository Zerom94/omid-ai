import asyncio
from core.manager import ManagerAgent

async def main():
    print("🚀 Testing Manager -> SecurityAgent Routing...")
    manager = ManagerAgent(config=None, memory=None) # مقادیر پیش‌فرض
    # دستوری که در داشبورد می‌نویسید را اینجا مستقیماً به مدیر می‌دهیم
    results = await manager.plan_and_dispatch("security scan https://example.com")
    
    print("\n" + "="*50)
    print("🎯 FINAL RESULTS:")
    print("="*50)
    for res in results:
        print(f"Task {res.task_id} | Success: {res.success}")
        if res.output:
            print(res.output)
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())
