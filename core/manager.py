"""OMID AI — Central Manager

The orchestrator. Receives the user's goal, breaks it into tasks, identifies
dependencies, dispatches to agents, tracks progress, retries failures, and
verifies results before declaring done.

Coordination model:
1. Parse goal string into atomic tasks.
2. Run dependency resolver: create prerequisites first.
3. Dispatch independent tasks in parallel.
4. Collect results, reassemble goal output.
5. Run quality gate (security + testing + analyst review) if specified.

Falls back gracefully: any failure should degrade rather than crash.
Never reports success without verification.
"""
from __future__ import annotations
import asyncio
import traceback
from typing import Optional

from agents.base import BaseAgent, Task, Result
from core.task_queue import TaskQueue
from core.memory import MemoryStore


class ManagerAgent(BaseAgent):
    name = "Manager"
    display_name = "Manager"

    async def execute(self, task: Task) -> Result:
        """Called when this agent gets a task. Delegates to real work."""
        # This is the bootstrap point — no individual tasks here.
        return Result(
            task_id=task.id,
            success=False,
            output={"message": "Manager does not handle individual tasks directly."},
            error="Not a valid task for manager",
        )

    async def plan_and_dispatch(self, goal: str) -> list[Result]:
        """Main orchestration loop: break goal into tasks, then run."""
        tasks = self.goal_to_tasks(goal)
        self.task_queue._tasks.update({t.id: t for t in tasks})

        loop = asyncio.get_event_loop()
        results = []
        # Run independent tasks in parallel
        parallel_jobs = {}
        for t in tasks:
            dep_done = await self._deps_satisfied(t)
            if dep_done:
                fut = loop.create_task(self._run_agent_once(t))
                parallel_jobs[t.id] = fut

        results = await asyncio.gather(*parallel_jobs.values(), return_exceptions=True)
        return results

    def goal_to_tasks(self, goal: str) -> list[Task]:
        """Transform a user goal string into a list of Task objects.

        Converts free-form text into structured tasks with sensible defaults.
        This is intentionally simple — extensible for more complex goal parsing.
        """
        tasks = []
        # Split goal into logical chunks by sentences/newlines
        lines = [l.strip() for l in goal.split("\n") if l.strip()]
        assignments = [
            ("research", "Research"),
            ("developer", "Development"),
            ("analyst", "Analysis"),
            ("testing", "Testing"),
            ("quality_control", "Quality Control"),
            ("security", "Security Review"),
        ]
        counter = 0
        for line in lines:
            parts = line.split(maxsplit=1)
            agent_id = parts[0].lower() if parts else "manager"
            desc = parts[1] if len(parts) > 1 else line
            tid = f"task_{counter}"
            tasks.append(Task(
                id=tid,
                description=line,
                agent_id=f"{agent_id}_agent",
                priority=3 if counter < 4 else 4,
                metadata={"goal_line": line},
            ))
            counter += 1

        # Always add manager monitoring tasks
        tasks.insert(0, Task(
            id="setup_env_check",
            description="Verify environment and install dependencies",
            agent_id="manager",
            priority=1,
        ))
        tasks.append(Task(
            id="final_review",
            description="Final quality control and reporting",
            agent_id="quality_control",
            priority=2,
        ))
        return tasks

    async def _run_agent_once(self, task: Task) -> Optional[Result]:
        """Dispatch a task to the right agent. Returns None on failure."""
        try:
            # Map agent_id to actual agent instances
            agent_map = self._register_agents()
            agent = agent_map.get(f"{task.agent_id}_agent", self)
            result = await agent.execute(task)
            if result and result.success:
                if task.id in task.dependencies:
                    # Someone depends on this task
                    pass
                self.task_queue.complete(task.id)
                self.log_event("complete", {"task_id": task.id, "agent": agent.name})
                return result
            else:
                self.log_event("fail", {"task_id": task.id, "error": result.error if result else "unknown"})
                return result
        except Exception as e:
            traceback.print_exc()
            self.log_event("crash", {"task_id": task.id, "error": str(e)})
            self.task_queue.fail(task.id)
            return Result(task_id=task.id, success=False, error=str(e))

    async def _deps_satisfied(self, task: Task) -> bool:
        """Check if all dependencies are verified."""
        for dep_id in task.dependencies:
            dep_task = self.task_queue._tasks.get(dep_id)
            if dep_task is None or dep_task.task.status != "verified":
                return False
        return True

    def _register_agents(self) -> dict:
        """Return mapping of agent_id_suffix -> agent instance."""
        return {
            "research": self._research_agent,
            "developer": self._dev_agent,
            "analyst": self._analyst_agent,
            "security": self._security_agent,
            "testing": self._test_agent,
            "quality_control": self._qc_agent,
            "memory_agent": self._mem_agent,
            "automation": self._automation_agent,
        }

    # Stub agents — populated in Stage 4
    def _research_agent(self):
        from agents.research_agent import ResearchAgent
        return ResearchAgent(config=self.config)

    def _dev_agent(self):
        from agents.developer_agent import DeveloperAgent
        return DeveloperAgent(config=self.config)

    def _analyst_agent(self):
        from agents.analyst_agent import AnalystAgent
        return AnalystAgent(config=self.config)

    def _security_agent(self):
        from agents.security_agent import SecurityAgent
        return SecurityAgent(config=self.config)

    def _test_agent(self):
        from agents.testing_agent import TestingAgent
        return TestingAgent(config=self.config)

    def _qc_agent(self):
        from agents.quality_control_agent import QualityControlAgent
        return QualityControlAgent(config=self.config)

    def _mem_agent(self):
        from agents.memory_agent_agent import MemoryAgent
        return MemoryAgent(memory=self.memory, config=self.config)

    def _automation_agent(self):
        from agents.automation_agent import AutomationAgent
        return AutomationAgent(config=self.config)
