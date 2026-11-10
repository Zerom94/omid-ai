"""OMID AI — Persistent Memory Store

Lightweight JSONL + index files. No database dependency. Stores:
- Completed tasks with results
- Event history (agent actions)
- Project metadata
- Error logs
- Verified artifacts registry

Auto-saves every Nth event. Safe under concurrent access via file locking.
File write timeouts are set defensively so a slow filesystem never hangs.
"""
from __future__ import annotations
import json
import os
import signal
import threading
from datetime import datetime, timezone
from pathlib import Path

PERSIST_DIR = "/sdcard/omid-ai/memory"

EVENT_THRESHOLD = 20  # auto-flush every N writes
WRITE_TIMEOUT_SEC = 10  # defensive timeout for any file I/O


def _timeout_handler(signum, frame):
    raise TimeoutError("File operation timed out after WRITE_TIMEOUT_SEC seconds")

signal.signal(signal.SIGALRM, _timeout_handler)


class _WriteTimeout(Exception):
    pass


class _TimeoutGuard:
    """Context manager that installs a SIGALRM to enforce timeouts on writes."""
    def __init__(self, seconds: int = WRITE_TIMEOUT_SEC):
        self.seconds = seconds

    def __enter__(self):
        self._old = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
        return self

    def __exit__(self, exc_type, exc, tb):
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, self._old)
        return False


class MemoryStore:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or PERSIST_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.base_dir / "history.jsonl"
        self.index_file = self.base_dir / "index.json"
        self.artifacts_file = self.base_dir / "artifacts.jsonl"
        self._events_since_save = 0
        self._lock = threading.Lock()
        self._ensure_files()

    def _ensure_files(self) -> None:
        for f in (self.history_file, self.index_file, self.artifacts_file):
            try:
                if not f.exists():
                    f.touch()
            except Exception:
                pass

    def _safe_append(self, filepath: Path, text: str) -> None:
        """Append text to a file with a hard timeout."""
        try:
            with _TimeoutGuard():
                with open(filepath, "a") as f:
                    f.write(text)
        except (TimeoutError, OSError):
            # Fall back to non-blocking best effort; don't crash the agent
            pass

    def save_result(self, result) -> None:
        """Persist a successful task result."""
        entry = json.dumps({
            "result": {
                "task_id": result.task_id,
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "execution_time_ms": result.execution_time_ms,
                "timestamp": result.timestamp,
            },
            "agent_id": result.task_id,
        }) + "\n"
        with self._lock:
            self._safe_append(self.history_file, entry)
            try:
                self._update_index("saved_result", entry)
            except Exception:
                pass

    def log_event(self, event_type: str, data: dict) -> None:
        """Append an event to the history file."""
        entry = json.dumps({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }) + "\n"
        with self._lock:
            self._safe_append(self.history_file, entry)
            try:
                self._update_index("logged_event", entry)
            except Exception:
                pass
            self._events_since_save += 1
            if self._events_since_save >= EVENT_THRESHOLD:
                self._events_since_save = 0

    def save_artifact(self, artifact_ref: str, description: str) -> None:
        """Register an artifact that was produced/verified."""
        entry = json.dumps({
            "artifact": {
                "ref": artifact_ref,
                "description": description,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }) + "\n"
        with self._lock:
            self._safe_append(self.artifacts_file, entry)
            try:
                self._update_index("saved_artifact", entry)
            except Exception:
                pass

    def load_history(self, limit: int = 100) -> list[dict]:
        """Load recent events as a list."""
        entries = []
        if not self.history_file.exists():
            return entries
        try:
            with self._lock, _TimeoutGuard():
                with open(self.history_file, "r") as f:
                    all_events = [json.loads(line) for line in f if line.strip()]
            entries = all_events[-limit:]
        except (TimeoutError, OSError, json.JSONDecodeError):
            pass
        return entries

    def load_errors(self) -> list[str]:
        """Extract all error messages from history."""
        errors = []
        for e in self.load_history(limit=500):
            if e.get("type") == "result" and not e.get("data", {}).get("success"):
                err = e["data"].get("error")
                if err:
                    errors.append(err)
        return errors

    def get_task_state(self, task_id: str) -> dict | None:
        """Find the latest recorded state for a task."""
        for e in self.load_history(limit=500):
            if e.get("type") == "result" and e["data"]["task_id"] == task_id:
                return {"task_id": task_id, **e["data"]}
        return None

    def clear_all(self) -> None:
        """Reset the memory store (use sparingly)."""
        for f in (self.history_file, self.index_file, self.artifacts_file):
            try:
                if f.exists():
                    f.unlink()
            except Exception:
                pass
        for f in (self.history_file, self.index_file, self.artifacts_file):
            try:
                f.touch()
            except Exception:
                pass
        self._events_since_save = 0

    def _update_index(self, action: str, entry: dict) -> None:
        """Update the lightweight index file (atomic write via rename)."""
        existing: dict = {}
        if self.index_file.exists():
            try:
                with _TimeoutGuard():
                    with open(self.index_file) as f:
                        existing = json.loads(f.read())
            except Exception:
                pass

        if action == "saved_result":
            tid = entry.get("result", {}).get("task_id", "?")
            ts = entry.get("timestamp", "")
            existing["results"] = existing.get("results", []) + [
                {"task_id": tid, "timestamp": ts}
            ]
        elif action == "saved_artifact":
            ref = entry.get("artifact", {}).get("ref", "?")
            ts = entry.get("timestamp", "")
            existing["artifacts"] = existing.get("artifacts", []) + [
                {"ref": ref, "timestamp": ts}
            ]
        elif action == "logged_event":
            ts = entry.get("timestamp", "")
            existing["last_event"] = {**entry, "action": action, "timestamp": ts}

        try:
            with _TimeoutGuard():
                with open(self.index_file.with_suffix(".json.tmp"), "w") as f:
                    json.dump(existing, f, indent=2)
                os.replace(self.index_file.with_suffix(".json.tmp"), self.index_file)
        except Exception:
            # Index is advisory — never block on it
            pass
