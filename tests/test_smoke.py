"""OMID AI — Smoke Tests

Minimal tests that verify core modules work. These are lightweight — no
mocking framework required. Just enough to catch syntax errors and import
failures before declaring the system ready.
"""
import sys
import os
import pytest

PROJECT_ROOT = "/sdcard/omid-ai"
sys.path.insert(0, PROJECT_ROOT)


def test_base_agent_imports():
    """BaseAgent class exists and is callable."""
    from agents.base import BaseAgent, Task, Result
    assert BaseAgent is not None
    assert Task is not None
    assert Result is not None


def test_manager_imports():
    """ManagerAgent can be imported."""
    from core.manager import ManagerAgent
    assert ManagerAgent is not None


def test_memory_store_init():
    """MemoryStore initializes without error."""
    from core.memory import MemoryStore
    ms = MemoryStore(base_dir=os.path.join(PROJECT_ROOT, "tests", "test_memory"))
    assert ms is not None
    ms.log_event("test_event", {"hello": "world"})
    ms.clear_all()


def test_task_queue_basic():
    """TaskQueue adds and completes tasks."""
    from core.task_queue import TaskQueue
    from agents.base import Task
    tq = TaskQueue()
    tq.add(Task(id="t1", description="first task", agent_id="dev"))
    next_t = tq.get_next()
    assert next_t is not None
    assert next_t.task.id == "t1"


def test_specialized_agents_exist():
    """All specialized agent classes can be imported."""
    from agents.research_agent import ResearchAgent
    from agents.developer_agent import DeveloperAgent
    from agents.analyst_agent import AnalystAgent
    from agents.security_agent import SecurityAgent
    from agents.testing_agent import TestingAgent
    from agents.automation_agent import AutomationAgent
    from agents.quality_control_agent import QualityControlAgent
    from agents.memory_agent_agent import MemoryAgent

    assert ResearchAgent is not None
    assert DeveloperAgent is not None
    assert AnalystAgent is not None
    assert SecurityAgent is not None
    assert TestingAgent is not None
    assert AutomationAgent is not None
    assert QualityControlAgent is not None
    assert MemoryAgent is not None


def test_cli_help():
    """CLI help command works."""
    from cli import run_command
    code = run_command("help", [])
    assert code == 0


def test_cli_unknown_command():
    """Unknown command returns non-zero."""
    from cli import run_command
    code = run_command("nope", [])
    assert code != 0


def test_cli_start_no_args():
    """Start without goal prints usage."""
    from cli import run_command
    code = run_command("start", [])
    assert code == 0


def test_cli_agents_lists():
    """The agents command lists available agents."""
    from cli import run_command
    code = run_command("agents", [])
    assert code == 0


def test_cli_status():
    """Status command succeeds."""
    from cli import run_command
    code = run_command("status", [])
    assert code == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
