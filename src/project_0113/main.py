#!/usr/bin/env python3
"""Simple persistent to‑do list.

Tasks are stored as a list of objects in ``tasks.json``::
    {"id": 1, "description": "Buy milk", "completed": false}
"""

import json
import argparse
from pathlib import Path
from itertools import count

DATA_FILE = Path(__file__).with_name("tasks.json")

def _load():
    """Return the list of tasks from the JSON file."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def _save(tasks):
    """Write the list of tasks to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, sort_keys=True)

def _next_id(tasks):
    """Generate the next integer id not used by existing tasks."""
    used = {t["id"] for t in tasks}
    for i in count(1):
        if i not in used:
            return i

def add(description):
    """Add a new task."""
    tasks = _load()
    task = {"id": _next_id(tasks), "description": description, "completed": False}
    tasks.append(task)
    _save(tasks)
    print(f"Added task {task['id']}.")

def list_tasks():
    """Print all tasks."""
    tasks = _load()
    if not tasks:
        print("No tasks.")
        return
    lines = (
        f"{t['id']}. [{'x' if t['completed'] else ' '}] {t['description']}"
        for t in tasks
    )
    print("\n".join(lines))

def complete(task_id):
    """Mark a task as completed."""
    tasks = _load()
    updated = False
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            updated = True
            break
    if updated:
        _save(tasks)
        print(f"Task {task_id} marked as completed.")
    else:
        print(f"Task {task_id} not found.")

def remove(task_id):
    """Remove a task."""
    tasks = _load()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found.")
        return
    _save(new_tasks)
    print(f"Task {task_id} removed.")

def main():
    parser = argparse.ArgumentParser(description="Command‑line todo list.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new task.")
    p_add.add_argument("description", nargs="+", help="Task description.")
    p_add.set_defaults(func=lambda ns: add(" ".join(ns.description)))

    p_list = sub.add_parser("list", help="List all tasks.")
    p_list.set_defaults(func=lambda ns: list_tasks())

    p_complete = sub.add_parser("complete", help="Mark a task as done.")
    p_complete.add_argument("id", type=int, help="Task id.")
    p_complete.set_defaults(func=lambda ns: complete(ns.id))

    p_remove = sub.add_parser("remove", help="Delete a task.")
    p_remove.add_argument("id", type=int, help="Task id.")
    p_remove.set_defaults(func=lambda ns: remove(ns.id))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
