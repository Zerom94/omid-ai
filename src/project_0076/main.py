#!/usr/bin/env python3
import argparse
from todo import add_task, list_tasks, complete_task, delete_task

def print_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "\u2714" if t["done"] else "\u2718"
        print(f"[{t['id']}] {status} {t['desc']}")

def main():
    parser = argparse.ArgumentParser(prog="todo", description="Simple command‑line to‑do list.")
    subparsers = parser.add_subparsers(dest="cmd")

    add = subparsers.add_parser("add", help="Add a new task")
    add.add_argument("description", nargs="+", help="Task description")

    ls = subparsers.add_parser("list", help="List tasks")
    ls.add_argument("-a", "--all", action="store_true", help="Show completed tasks as well")

    done = subparsers.add_parser("done", help="Mark a task as completed")
    done.add_argument("id", type=int, help="Task ID")

    rm = subparsers.add_parser("rm", help="Delete a task")
    rm.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.cmd == "add":
        desc = " ".join(args.description)
        add_task(desc)
        print(f'Added task: "{desc}"')
    elif args.cmd == "list":
        tasks = list_tasks(show_all=args.all)
        print_tasks(tasks)
    elif args.cmd == "done":
        if complete_task(args.id):
            print(f"Task {args.id} marked as done.")
        else:
            print(f"No task with ID {args.id}.")
    elif args.cmd == "rm":
        if delete_task(args.id):
            print(f"Task {args.id} deleted.")
        else:
            print(f"No task with ID {args.id}.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
