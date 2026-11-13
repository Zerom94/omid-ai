import json
import os
from typing import List, Dict

DATA_FILE = os.path.join(os.path.expanduser("~"), ".todo_data.json")

def load_tasks() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def add_task(description: str) -> None:
    tasks = load_tasks()
    tasks.append({"id": max([t["id"] for t in tasks], default=0) + 1, "desc": description, "done": False})
    save_tasks(tasks)

def list_tasks(show_all: bool = False) -> List[Dict]:
    tasks = load_tasks()
    if not show_all:
        tasks = [t for t in tasks if not t["done"]]
    return tasks

def complete_task(task_id: int) -> bool:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            return True
    return False

def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return False
    save_tasks(new_tasks)
    return True
