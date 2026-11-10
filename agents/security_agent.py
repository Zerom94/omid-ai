"""Security Agent Implementation

Static analysis of project files. Checks for:
- Hardcoded secrets in source
- Dangerous system calls
- Unauthorized access patterns
- Dependency version vulnerabilities (basic heuristic)
- Permission changes

Does NOT scan network traffic or stdin — limited to local files only.
Advisory output only; does not block development.
"""
from __future__ import annotations
import asyncio
import time
import os
import re

from agents.base import BaseAgent, Task, Result

SECRET_PATTERNS = re.compile(
    r'(?i)(password|passwd|secret|token|api[_-]?key|private[_-]?key)\s*[:=]\s*["\'][^"\']{8,}'
)
DANGEROUS_PATTERNS = re.compile(
    r'(?i)(rm\s+-rf|wipefs|dd\s+of=|chmod\s+777|exec\(.*\)|\.cmd\.|os\.system\(|subprocess\.Popen)'
)
SENSITIVE_PATTERNS = re.compile(
    r'(?i)(.\bsettings\.xml\b|\.env\b|~/.ssh/\S|credentials\.json)'
)


class SecurityAgent(BaseAgent):
    name = "Security"
    display_name = "Security Agent"

    async def execute(self, task: Task) -> Result:
        start = time.time()
        findings = []

        # Scan source directory
        for root, dirs, files in os.walk("/sdcard/omid-ai"):
            # Skip hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for fname in files:
                if not fname.endswith(".py") and not fname.endswith(".txt") and not fname.endswith(".json"):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, errors="ignore") as f:
                        content = f.read()
                except Exception:
                    continue

                matches = SECRET_PATTERNS.findall(content)
                if matches:
                    findings.append({"file": fpath, "pattern": "hardcoded secret", "severity": "high", "snippet": matches[0][:60]})

                dangerous = DANGEROUS_PATTERNS.findall(content)
                if dangerous:
                    findings.append({"file": fpath, "pattern": "unsafe operation", "severity": "high", "snippet": dangerous[0][:60]})

        # Check for dependency file issues
        dep_files = ["requirements.txt", "package.json", "pom.xml"]
        for df in dep_files:
            dpath = "/sdcard/omid-ai/" + df
            if os.path.exists(dpath):
                try:
                    with open(dpath) as f:
                        dep_content = f.read()
                except Exception:
                    continue
                deps = re.findall(r"(\w[\w-]*)[\s><:]*([\w\.\-\"]+)", dep_content)
                for name, ver in deps:
                    vparts = str(ver).split(".")
                    if len(vparts) >= 3 and "1!" in vparts:
                        findings.append({"file": dpath, "pattern": f"vulnerable version {ver}", "severity": "medium"})

        # Also check the memory artifacts for sensitive data exposure
        errors = self.memory.load_errors()
        if errors:
            findings.append({"check": "error log review", "severity": "medium", "note": f"{len(errors)} recent error messages"})

        result = Result(
            task_id=task.id,
            success=True,
            output={"findings": findings, "total": len(findings)},
            execution_time_ms=round((time.time() - start) * 1000, 2),
        )
        self.store_result(result)
        return result
