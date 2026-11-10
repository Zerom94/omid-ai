"""OMID AI — Base Agent Interface

Every specialized agent inherits from this. Defines the contract:
- Each agent receives a Task object and returns a Result object.
- Agents are stateless within a task; state lives in the memory layer.
- Agents must log their activity to the memory store on significant events.
"""
from __future__ import annotations
import abc
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class Task:
    """A single unit of work assigned to an agent."""
    id: str
    description: str
    agent_id: str          # which agent handles it
    priority: int = 5      # 1 = highest
    status: str = "pending" # pending | queued | in_progress | verified | failed | dead
    dependencies: list[str] = field(default_factory=list)  # task ids this depends on
    result: Optional[dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    created_at: str = ""
    completed_at: str = ""
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class Result:
    """Output from an agent completing a task."""
    task_id: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BaseAgent(abc.ABC):
    """Base class for all OMID AI agents."""

    name: str = "BaseAgent"
    display_name: str = "Base Agent"

    def __init__(self, task_queue=None, memory=None, config=None):
        self.task_queue = task_queue      # TaskQueue instance or None
        self.memory = memory              # MemoryStore instance or None
        self.config = config or {}        # system configuration dict

    @abc.abstractmethod
    async def execute(self, task: Task) -> Result:
        """Execute one task. Must be implemented by subclasses."""
        raise NotImplementedError

    def store_result(self, result: Result) -> None:
        """Persist this result to the memory store if available."""
        if self.memory is not None:
            self.memory.save_result(result)

    def log_event(self, event_type: str, data: dict) -> None:
        """Record significant events for project history."""
        if self.memory is not None:
            self.memory.log_event(f"{self.name}.{event_type}", data)
