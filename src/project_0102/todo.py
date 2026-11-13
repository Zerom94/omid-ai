import sys
from storage import load_tasks, save_tasks

class TodoApp:
    def __init__(self):
        self.tasks = load_tasks()

    def run(self):
        while True:
            self.print_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.list_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.complete_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.save_and_exit()
            else:
                print("Invalid choice.")

    def print_menu(self):
        print("\nTodo List")
        print("1) List tasks")
        print("2) Add task")
        print("3) Complete task")
        print("4) Delete task")
        print("5) Save and exit")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks.")
            return
        for idx, task in enumerate(self.tasks, 1):
            status = "✔" if task["done"] else "✘"
            print(f"{idx}. [{status}] {task['title']}")

    def add_task(self):
        title = input("Task title: ").strip()
        if title:
            self.tasks.append({"title": title, "done": False})
            print("Task added.")
        else:
            print("Title cannot be empty.")

    def complete_task(self):
        self.list_tasks()
        idx = input("Enter task number to complete: ").strip()
        if idx.isdigit():
            i = int(idx) - 1
            if 0 <= i < len(self.tasks):
                self.tasks[i]["done"] = True
                print("Task marked as done.")
                return
        print("Invalid task number.")

    def delete_task(self):
        self.list_tasks()
        idx = input("Enter task number to delete: ").strip()
        if idx.isdigit():
            i = int(idx) - 1
            if 0 <= i < len(self.tasks):
                del self.tasks[i]
                print("Task deleted.")
                return
        print("Invalid task number.")

    def save_and_exit(self):
        save_tasks(self.tasks)
        print("Tasks saved. Bye!")
        sys.exit(0)
