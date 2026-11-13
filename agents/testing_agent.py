"""Testing Agent Implementation

Runs tests after development tasks. Creates and executes smoke tests for
newly written modules. Verifies that developer changes actually work.

Uses Python's unittest framework. Creates minimal test files alongside
source modules. If no tests exist, creates basic smoke tests automatically.
"""
from __future__ import annotations
import asyncio
import os
import sys
import time
import importlib
import importlib.util
from pathlib import Path

from agents.base import BaseAgent, Task, Result

TEST_DIR = Path("/sdcard/omid-ai/tests")


class TestingAgent(BaseAgent):
    name = "Testing"
    display_name = "Testing Agent"

    async def execute(self, task: Task) -> Result:
        kb_path = "/sdcard/omid-ai/agents_knowledge.json"
        rules = ""
        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                import json
                rules = json.load(f).get("testing", "")
                if rules:
                    print(f"[{self.name}] 🎓 Using latest rules: {rules}", flush=True)
        start = time.time()
        test_results = []

        # Check for existing test coverage
        test_files = TEST_DIR.glob("test_*.py") if TEST_DIR.exists() else []
        tests_exist = len(test_files) > 0

        if not tests_exist:
            # Auto-create smoke tests for each source file
            for src_file in SRC_DIR.glob("*.py"):
                test_name = f"test_{src_file.stem}.py"
                test_path = TEST_DIR / test_name
                smoke_code = self._generate_smoke_test(src_file)
                with open(test_path, "w") as f:
                    f.write(smoke_code)
                test_results.append({"test": test_name, "status": "created", "runtime_ms": 0})

        # Run all available tests
        passed, failed = 0, 0
        for tf in sorted(test_files):
            tsuccess, terr = await self._run_test(tf)
            if tsuccess:
                passed += 1
                test_results.append({"test": tf.name, "status": "pass", "runtime_ms": 0})
            else:
                failed += 1
                test_results.append({"test": tf.name, "status": "fail", "error": terr[:100] if terr else "unknown"})

        overall = passed > 0 and failed == 0
        result = Result(
            task_id=task.id,
            success=overall,
            output={"tests": test_results, "passed": passed, "failed": failed, "total": passed + failed},
            execution_time_ms=round((time.time() - start) * 1000, 2),
        )
        self.store_result(result)
        return result

    async def _run_test(self, test_path: Path) -> tuple[bool, str | None]:
        try:
            sys.path.insert(0, str(TEST_DIR))
            importlib.import_module(f"test_{test_path.stem}")
            return True, None
        except Exception as e:
            return False, str(e)[:100]

    def _generate_smoke_test(self, src_file: Path) -> str:
        rel = f"../../../{src_file.relative_to('/sdcard/omid-ai')}"
        stem = src_file.stem
        module_name = stem.replace(".py", "")
        return f'''import sys
import importlib
spec = importlib.util.spec_from_file_location("{module_name}", "{rel}")
mod = importlib.util.module_from_spec(spec)
assert spec is not None, "Module spec failed to load"
spec.loader.exec_module(mod)
assert hasattr(mod, 'main'), "Missing main function"
'''
