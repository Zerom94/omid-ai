#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

# Path to the JSON file that stores tasks (placed beside this script)
TASKS_FILE = Path(__file__).with_name('tasks.json')


def load_tasks():
    """Load tasks from the JSON file, returning a list (empty if file missing or corrupt)."""
    if TASKS_FILE.is_file():
        try:
            return json.loads(TASKS_FILE.read_text())
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(tasks):
    """Persist the given task list to the JSON file with pretty formatting."""
    TASKS_FILE.write_text(json.dumps(tasks, indent=2, sort_keys=True))


def get_next_id(tasks):
    """Return a new unique id (max existing id + 1, or 1 if none)."""
    return max((t['id'] for t in tasks), default=0) + 1


def add_task(description):
    tasks = load_tasks()
    task = {'id': get_next_id(tasks), 'description': description, 'completed': False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {task['id']}.")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    # Lazy generation of formatted lines, then join once for output
    lines = (f"{t['id']}. [{'x' if t['completed'] else ' '}] {t['description']}" for t in tasks)
    sys.stdout.write('\n'.join(lines) + '\n')


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['completed'] = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed.")
            return
    print(f"Task {task_id} not found.", file=sys.stderr)


def delete_task(task_id):
    tasks = load_tasks()
    # List comprehension creates a new list without the target task (lazy filter)
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found.", file=sys.stderr)
    else:
        save_tasks(new_tasks)
        print(f"Task {task_id} deleted.")


def main():
    parser = argparse.ArgumentParser(description="Simple TODO CLI")
    subparsers = parser.add_subparsers(dest='command')

    # add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', nargs='+', help='Task description')

    # list command
    subparsers.add_parser('list', help='List all tasks')

    # complete command
    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('id', type=int, help='ID of the task to complete')

    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='ID of the task to delete')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(' '.join(args.description))
    elif args.command == 'list':
        list_tasks()
    elif args.command == 'complete':
        complete_task(args.id)
    elif args.command == 'delete':
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
