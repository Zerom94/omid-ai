# Memory Agent

Persistent local store for project history. Stores completed tasks, decisions,
pending work, error logs, and verified results. Enables resume after interruption.

Storage: JSONL files in ./memory/history.jsonl + index.json for fast lookups.
Thread-safe with file locking. Auto-saves important progress every N steps.
Coordinates with the manager to update task records on completion.

Implements BaseAgent. No agent-specific logic beyond storage and retrieval.
