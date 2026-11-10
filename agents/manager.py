# OMID AI — Central Manager Agent

The central orchestrator. Breaks goals into tasks, tracks dependencies, runs
parallel work, retries failures, and verifies results before reporting done.

Subclasses agents.Agent when specialized logic is needed; inherits from
**BaseAgent**. Handles task queue management and coordination between agents.

Task lifecycle states: pending -> queued -> in_progress -> verified / failed
                                  \-> retry -> re-verified | dead  (max retries)
Stores provenance: which agent did what, with what results, when.
Deduplicates by task_id.

No persistence beyond memory agent state unless explicitly requested.
Never claims a task complete without verification.
