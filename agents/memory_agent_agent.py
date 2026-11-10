"""Memory Agent Implementation

Wraps the PersistentMemoryStore to provide agent-level state management.
Stores completed tasks, decisions, pending work, and verified results.
Enables resume after interruption. This is the agent interface to the store.
"""
from __future__ import annotations
import asyncio
import json
import time
from pathlib import Path
from typing import Any

from agents.base import BaseAgent, Task, Result
from core.memory import MemoryStore


class MemoryAgent(BaseAgent):
    name = "Memory"
    display_name = "Memory Agent"

    async def execute(self, task: Task) -> Result:
        """Handle memory-related tasks: save result, log event, query state."""
        action = task.description.strip().lower().split()[0] if task.description.strip() else "noop"
        self.log_event("execute", {"task_id": task.id, "action": action, "description": task.description})

        if action in ("save", "record", "store"):
            return await self._save_result(task)
        elif action in ("log", "event"):
            return await self._log_event(task)
        elif action in ("query", "check", "state"):
            return await self._query_state(task)
        elif action in ("clear", "reset"):
            self.memory.clear_all()
            self.store_result(Result(task_id=task.id, success=True, output={"cleared": True}))
            return self.store_result(Result(task_id=task.id, success=True, output={"cleared": True}))
        else:
            result = Result(task_id=task.id, success=False, error="Unknown memory action")
            self.store_result(result)
            return result

    async def _save_result(self, task: Task) -> Result:
        # Results get saved automatically by the other agents via store_result().
        # This is a no-op re-entry point for explicit saves.
        self.store_result(Result(task_id=task.id, success=True, output={"auto_saved": True}))
        return self.store_result(Result(task_id=task.id, success=True, output={"auto_saved": True}))

    async def _log_event(self, task: Task) -> Result:
        event_type = task.description.strip().split(maxsplit=1)[0].lower()
        self.memory.log_event(event_type, {
            "task_id": task.id,
            "description": task.description,
        })
        self.log_event("log_written", {"task_id": task.id})
        return self.store_result(Result(task_id=task.id, success=True, output={"logged": event_type}))

    async def _query_state(self, task: Task) -> Result:
        q_type = " ".join(task.description.strip().split()[0:2])
        q_type = q_type.lower()
        if "history" in q_type or "project" in q_type:
            entries = self.memory.load_history(limit=50)
            return self.store_result(Result(
                task_id=task.id,
                success=True,
                output={"entries": len(entries), "sample": entries[-3:] if entries else []},
            ))
        elif "errors" in q_type or "error" in q_type:
            errors = self.memory.load_errors()
            return self.store_result(Result(
                task_id=task.id,
                success=True,
                output={"count": len(errors), "examples": errors[:5]},
            ))
        else:
            state = self.memory.get_task_state(task.id)
            return self.store_result(Result(
                task_id=task.id,
                success=True,
                output={"task_state": state},
            ))
