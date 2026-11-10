"""OMID AI — CLI Command Interface

Commands:
  omid start "your goal here"      Launch the agent team
  omid status                       Show task queue and project state
  omid tasks                         List all known tasks
  omid agents                        List available agents
  omid pause                         Pause execution
  omid resume                         Resume paused tasks
  omid memory                        Show project memory history
  omid help                          Show this help message
  omid reset                         Clear project memory (dangerous)
"""
from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path
from core.memory import MemoryStore

PROJECT_DIR = Path("/sdcard/omid-ai")

COMMANDS = {
    "start": "Run the agent team on your goal",
    "status": "Show task queue and project state",
    "tasks": "List all known tasks",
    "agents": "List available agents",
    "pause": "Pause execution (saves state)",
    "resume": "Resume paused tasks",
    "memory": "Show project memory history",
    "help": "Show this help message",
    "reset": "Clear project memory — requires confirmation",
}


def run_command(cmd: str, args: list[str]) -> int:
    if cmd == "help" or cmd == "--help":
        print(_HELP_TEXT)
        return 0

    if not cmd:
        print("Usage: omid <command> [args...]")
        print(f"Available commands:")
        for name, desc in COMMANDS.items():
            print(f"  {name:<10} {desc}")
        return 0

    handler = _HANDLERS.get(cmd)
    if handler is None:
        print(f"Unknown command: '{cmd}'")
        print(f"Type 'omid help' for available commands.")
        return 1
    if cmd == "reset":
        try:
            confirm = input("This will permanently delete all OMID AI memory. Continue? [y/N]: ").strip().lower()
            if confirm != "y":
                print("Cancelled.")
                return 0
        except EOFError:
            print("Cancelled (no input).")
            return 0
        finally:
            import shutil
            shutil.rmtree(PROJECT_DIR / "memory", ignore_errors=True)
            print("Memory cleared.")
        return 0

    handler(args)
    return 0


def _start(args):
    if len(args) < 1:
        print("Usage: omid start \"your goal description\"")
        print("Example: omid start \"Build a Python todo app\"")
        return
    goal = " ".join(args)
    print(f"[START] Goal received: {goal[:80]}{'...' if len(goal) > 80 else ''}")
    # Quick pre-flight checks
    print("[PRE-FLIGHT] Checking project structure...")
    checks = [
        PROJECT_DIR.exists(),
        (PROJECT_DIR / "core").is_dir(),
        (PROJECT_DIR / "agents").is_dir(),
        (PROJECT_DIR / "agents" / "base.py").exists(),
    ]
    for i, ok in enumerate(checks):
        print(f"  {'OK' if ok else 'FAIL'} check {i+1}: {'Project structure present' if ok else 'MISSING'}")
    asyncio.run(_dispatch(goal))


def _status(args):
    """Show task queue and project state."""
    info = {}
    if PROJECT_DIR.exists():
        info["project_dir"] = str(PROJECT_DIR)
        for f in ("src", ".omid.toml"):
            p = PROJECT_DIR / f
            info[f"{f}"] = p.exists()
    # Show memory-based stats
    mem = MemoryStore(base_dir=str(PROJECT_DIR / "memory"))
    recent = mem.load_history(limit=10)
    info["recent_tasks"] = recent
    info["total_memory_events"] = len(mem.load_history())
    info["error_count"] = len(mem.load_errors())
    print(json.dumps(info, indent=2, default=str))


def _tasks(args):
    """List tasks from memory store."""
    mem = MemoryStore(base_dir=str(PROJECT_DIR / "memory"))
    entries = mem.load_history(limit=200)
    print(f"Found {len(entries)} recent records in memory store.")
    for e in entries[-15:]:
        if e.get("type") == "result":
            r = e.get("data", {})
            icon = "✓" if r.get("success") else "✗"
            err = r.get("error", "")[:60] if not r.get("success") else ""
            print(f"  {icon} [{e.get('timestamp','')[:19]}] task={r.get('task_id', '?')} err={err}")


def _agents(args):
    """List all registered agent names."""
    agent_files = sorted([
        f.name.replace(".py", "")
        for f in PROJECT_DIR.glob("agents/*_agent.py")
    ])
    print(f"Available OMID AI agents ({len(agent_files)}):")
    for i, name in enumerate(agent_files, 1):
        print(f"  {i}. {name}")


def _pause(args):
    print("[PAUSE] State is already saved in memory store. Execution continues when you run 'omid resume'.")


def _resume(args):
    print("[RESUME] Rebuilding task queue from memory. Restarting manager.")
    import asyncio
    from core.manager import ManagerAgent
    from core.memory import MemoryStore
    mem = MemoryStore(base_dir=str(PROJECT_DIR / "memory"))
    mgr = ManagerAgent(task_queue=TaskQueue(), memory=mem, config={})
    asyncio.run(mgr.plan_and_dispatch("resume from memory"))


def _memory(args):
    """Show memory history."""
    mem = MemoryStore(base_dir=str(PROJECT_DIR / "memory"))
    entries = mem.load_history(limit=50)
    print(f"[MEMORY] {len(entries)} events recorded:")
    for e in entries[-20:]:
        etype = e.get("type", "")
        data = e.get("data", {})
        ts = e.get("timestamp", "")[:19]
        detail = ""
        if etype == "result":
            ok = data.get("success")
            icon = "[OK]" if ok else "[FAIL]"
            tid = data.get("task_id", "?")
            detail = f"{icon} {tid}"
            if not ok:
                err = data.get("error", "")[:60]
                detail += f" error: {err}"
        elif etype == "crash":
            detail = f"[CRASH] {data.get('task_id', '?')}: {data.get('error', '')[:80]}"
        else:
            detail = f"[{etype}] {json.dumps(data, default=str)[:80]}"
        print(f"  {ts}  {detail}")


_HANDLERS = {
    "start": _start,
    "status": _status,
    "tasks": _tasks,
    "agents": _agents,
    "pause": _pause,
    "resume": _resume,
    "memory": _memory,
}

_HELP_TEXT = """
OMID AI — Autonomous Multi-Agent System
========================================

Commands:
  omid start "goal"          Launch the team on your goal
  omid status                Show task queue and project state
  omid tasks                 List tasks and results from memory
  omid agents               List available agents
  omid pause                Show current state (state auto-saved)
  omid resume                Resume after interruption
  omid memory                Show memory history and events
  omid help                  Show this help
  omid reset                Clear ALL memory (permanent — use sparingly)

Example:
  omid start "Create a CLI tool for file management"
  omid status
  omid tasks
  omid memory

NOTE: System saves persistent memory automatically. No data is lost between runs.
Budget: $0 (all agents are free/open-source).
Platform: Android + Termux.
"""
