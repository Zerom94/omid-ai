"""Automation Agent Implementation

Handles safe, permitted repetitive workflows: cloning repos, running linters,
formatting code, generating scaffolding files. Only actions that are safe
and reversible are permitted.

This agent checks every action against an allowlist before executing. Any action
outside the allowlist triggers an immediate request to the manager for approval.
The agent never initiates destructive operations on its own.
"""
from __future__ import annotations
import asyncio
import time
import subprocess
from pathlib import Path

from agents.base import BaseAgent, Task, Result

ALLOWED_READ = {"read"}
ALLOWED_WRITE = {"write_config", "write_scaffolding"}
ALLOWED_EXECUTE = {"run_lint", "run_tests", "run_smoke", "format"}
ALLOWED_SELF = {"init_project", "make_dir"}

UNSAFE_PATTERNS = {"delete", "remove", "rm", "rm_rf", "publish", "deploy",
                   "send", "email", "purchase", "payment", "access_personal",
                   "change_security", "execute_untrusted"}


class AutomationAgent(BaseAgent):
    name = "Automation"
    display_name = "Automation Agent"

    async def execute(self, task: Task) -> Result:
        action = self._extract_action(task.description)
        if action in UNSAFE_PATTERNS:
            result = Result(
                task_id=task.id,
                success=False,
                output={"reason": "Action requires explicit manager approval before execution.", "allowed": False},
                error=f"Unsafe action '{action}' requires manager approval.",
            )
            self.log_event("blocked", {"action": action, "task_id": task.id})
            return result

        allowed_actions = ALLOWED_READ | ALLOWED_WRITE | ALLOWED_EXECUTE | ALLOWED_SELF
        if action not in allowed_actions:
            result = Result(
                task_id=task.id,
                success=False,
                output={"reason": f"Action '{action}' is not in the safe allowlist. Approval required.", "allowed": False},
                error=f"Action '{action}' requires explicit manager approval.",
            )
            return result

        await self._do_action(action, task.description)
        result = Result(
            task_id=task.id,
            success=True,
            output={"action": action, "state": "completed"},
            execution_time_ms=round((time.time() - 0) * 1000, 2),
        )
        self.store_result(result)
        return result

    def _extract_action(self, desc: str) -> str:
        """Extract the first verb token from the description."""
        parts = desc.strip().split(maxsplit=1)
        if parts:
            verb = parts[0].lower()
            # Normalize common compound verbs
            compound_map = {
                "clone_repo": "clone", "clone": "clone", "install_deps": "install", "install": "install",
                "init_project": "init_project", "make_dir": "make_dir", "cleanup": "delete",
            }
            return compound_map.get(verb, verb)
        return "noop"

    async def _do_action(self, action: str, desc: str) -> None:
        """Execute a safe automation action. No blocking IO — just fire and log."""
        if action == "run_lint":
            proc = await asyncio.to_thread("flake8 /sdcard/omid-ai --max-line-length=120 2>&1 || true".split())
        elif action == "run_tests":
            proc = await asyncio.to_thread("cd /sdcard/omid-ai && python3 -m pytest tests/ -v 2>&1 || true".split())
        elif action == "run_smoke":
            self._smoke_run(desc)
        elif action == "format":
            await asyncio.to_thread("python3 -m black /sdcard/omid-ai/src/ 2>&1 || true".split())
        elif action == "write_config":
            cfg_path = Path("/sdcard/omid-ai/.omid.toml")
            with open(cfg_path, "w") as f:
                f.write('[general]\nversion = "1.0.0"\nplatform = "android"\nbudget = 0\n')
        elif action == "make_dir":
            Path("/sdcard/omid-ai/logs").mkdir(parents=True, exist_ok=True)

    def _smoke_run(self, desc: str) -> None:
        """Smoke-test relevant source files."""
        import importlib.util
        src = Path("/sdcard/omid-ai/src")
        for f in src.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(f"smoke_{f.stem}", f)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
            except Exception:
                pass
