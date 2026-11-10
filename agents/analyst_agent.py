"""Analyst Agent Implementation

Analyzes research findings, requirements, test results, and development outputs.
Identifies gaps, risks, inconsistencies. Suggests solutions.

Output is advisory — does not block the workflow.
"""
from __future__ import annotations
import time

from agents.base import BaseAgent, Task, Result


class AnalystAgent(BaseAgent):
    name = "Analyst"
    display_name = "Analyst Agent"

    async def execute(self, task: Task) -> Result:
        start = time.time()
        findings = []

        # Analyze previous task results for gaps and risks
        history = self.memory.load_history(limit=200)
        failures = [e for e in history if e.get("type") == "result" and not e["data"].get("success")]
        security_flags = self._scan_for_security_patterns(failures)
        test_failures = self._scan_test_failures(history)

        findings.extend([
            {
                "finding": f"N={len(failures)} task failure(s) detected in recent history",
                "severity": "medium" if len(failures) < 3 else "high",
                "recommendation": "Review failed tasks and their error messages before proceeding.",
            },
            {
                "finding": f"Security pattern scan: {len(security_flags)} potential issues",
                "severity": "high" if security_flags else "low",
                "recommendation": security_flags or "No obvious security red flags found.",
            },
        ])

        result = Result(
            task_id=task.id,
            success=True,
            output={"analysis": findings},
            execution_time_ms=round((time.time() - start) * 1000, 2),
        )
        self.store_result(result)
        return result

    def _scan_for_security_patterns(self, failures: list[dict]) -> list[str]:
        flags = []
        for f in failures:
            err = f.get("data", {}).get("error", "")
            if any(kw in err.lower() for kw in ("secret", "password", "token", "api key", "permission", "auth", "exec ")):
                flags.append(f"Potential secret/config leak in error: {err[:80]}...")
        return flags

    def _scan_test_failures(self, history: list[dict]) -> list[str]:
        flags = []
        for e in history[-50:]:
            data = e.get("data", {})
            if data.get("error"):
                flags.append(f"Test failure: {str(data.get('error'))[:80]}")
        return flags
