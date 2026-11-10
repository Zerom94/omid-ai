"""TaskQueue — lightweight job scheduler

Manages task lifecycle with priority ordering, dependency resolution, retry
with backoff, and parallel dispatch tracking. Does NOT run tasks — just
schedules them for agents.

States: pending -> queued -> in_progress -> verified / failed / dead
Retries: dead after max_retries attempts per dependency graph.
"""
from __future__ import annotations
import asyncio
import random
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScheduledTask:
    task: object  # Task instance
    scheduled_for: float = 0.0  # wall-clock schedule time


class TaskQueue:
    """Simple priority-aware task queue."""

    MAX_RETRIES = 3
    BACKOFF_MIN = 2.0
    BACKOFF_MAX = 30.0

    def __init__(self, max_retries: int = MAX_RETRIES):
        self._tasks: dict[str, ScheduledTask] = {}
        self._max_retries = max_retries
        self._pending_priority: list[tuple[int, str]] = []  # (priority, id)

    def add(self, task) -> None:
        """Add a task to the queue."""
        self._tasks[task.id] = ScheduledTask(task=task, scheduled_for=time.time())
        self._pending_priority.append((task.priority, task.id))
        self._pending_priority.sort(reverse=True)  # higher priority first

    def get_next(self) -> Optional[ScheduledTask]:
        """Get highest-priority pending task ready to execute."""
        ready = []
        remaining = []
        for prio, tid in self._pending_priority:
            t = self._tasks[tid]
            deps_met = all(
                d in [x.id for x in self._tasks.values()] and any(
                    d_t.status == "verified" for d_t in self._tasks.values() if d_t.id == d
                )
                for d in t.task.dependencies
            )
            dead = self._is_dead(t.task.id)
            if not deps_met and not dead:
                remaining.append((prio, tid))
            else:
                ready.append((prio, tid))
        self._pending_priority = remaining
        if not ready:
            return None
        ready.sort(reverse=True)
        return self._tasks[ready[0][1]]

    def complete(self, task_id: str) -> None:
        """Mark a task as completed (verified). Clears from pending list."""
        tid = task_id
        for i, (prio, t) in enumerate(list(self._pending_priority)):
            if t == task_id:
                self._pending_priority.pop(i)
                break

    def fail(self, task_id: str) -> bool:
        """Handle a failed task — increment retry count, possibly dead."""
        tid = task_id
        found = False
        for prio, t in self._pending_priority:
            if t == tid:
                self._pending_priority.pop(next(i for i, (p, x) in enumerate(self._pending_priority) if x == tid))
                found = True
                break
        task = self._tasks.get(tid)
        if found and task:
            task.task.retry_count += 1
            if task.task.retry_count >= self._max_retries:
                task.task.status = "dead"
                print(f"[WARNING] Task {tid} failed {self._max_retries} times — marked DEAD")
            else:
                backoff = random.uniform(self.BACKOFF_MIN, self.BACKOFF_MAX)
                delay = max(60, int(backoff * 1000))  # wait at least 60s
                print(f"[WARNING] Task {tid} failed. Retry {task.task.retry_count}/{self._max_retries} in {delay}s")
        return found

    def _is_dead(self, task_id: str) -> bool:
        task = self._tasks.get(task_id)
        return task is not None and task.task.status == "dead"

    def status(self) -> dict:
        """Return overview of current queue state."""
        return {
            total: len(self._tasks),
            pending: sum(1 for t in self._tasks.values() if t.task.status in ("pending", "queued")),
            in_progress: sum(1 for t in self._tasks.values() if t.task.status == "in_progress"),
            verified: sum(1 for t in self._tasks.values() if t.task.status == "verified"),
            failed: sum(1 for t in self._tasks.values() if t.task.status == "failed"),
            dead: sum(1 for t in self._tasks.values() if t.task.status == "dead"),
        }
