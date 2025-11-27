"""
Advanced Project: Task Manager
-------------------------------
A command-line task manager that combines: classes, file handling, error handling,
and data structures. Tasks are saved to a JSON file.
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class Task:
    """Represents a single task."""
    
    def __init__(self, title: str, description: str = "", priority: str = "medium"):
        self.title = title
        self.description = description
        self.priority = priority  # low, medium, high
        self.completed = False
        self.created_at = datetime.now().isoformat()
    
    def mark_complete(self):
        """Mark task as completed."""
        self.completed = True
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON storage."""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create Task from dictionary."""
        task = cls(data["title"], data.get("description", ""), data.get("priority", "medium"))
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", datetime.now().isoformat())
        return task
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} [{self.priority.upper()}] {self.title}"


class TaskManager:
    """Manages a collection of tasks with file persistence."""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.filename, "w") as file:
                data = [task.to_dict() for task in self.tasks]
                json.dump(data, file, indent=2)
        except IOError as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, title: str, description: str = "", priority: str = "medium"):
        """Add a new task."""
        task = Task(title, description, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added: {task}")
    
    def list_tasks(self, show_completed: bool = True):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks found.")
            return
        
        print("\n=== Your Tasks ===")
        for i, task in enumerate(self.tasks, 1):
            if show_completed or not task.completed:
                print(f"{i}. {task}")
    
    def complete_task(self, index: int):
        """Mark a task as completed."""
        try:
            task = self.tasks[index - 1]
            task.mark_complete()
            self.save_tasks()
            print(f"Task completed: {task.title}")
        except IndexError:
            print("Invalid task number.")
    
    def delete_task(self, index: int):
        """Delete a task."""
        try:
            task = self.tasks.pop(index - 1)
            self.save_tasks()
            print(f"Task deleted: {task.title}")
        except IndexError:
            print("Invalid task number.")


def main():
    """Main program loop."""
    manager = TaskManager()
    
    while True:
        print("\n=== Task Manager ===")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ").strip()
        
        if choice == "1":
            title = input("Task title: ").strip()
            description = input("Task description (optional): ").strip()
            priority = input("Priority (low/medium/high) [medium]: ").strip().lower()
            if priority not in ["low", "medium", "high"]:
                priority = "medium"
            manager.add_task(title, description, priority)
        
        elif choice == "2":
            manager.list_tasks()
        
        elif choice == "3":
            manager.list_tasks()
            try:
                index = int(input("\nEnter task number to complete: "))
                manager.complete_task(index)
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == "4":
            manager.list_tasks()
            try:
                index = int(input("\nEnter task number to delete: "))
                manager.delete_task(index)
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

# --- Your turn --------------------------------------------------------------
# 1. Add a feature to filter tasks by priority.
# 2. Add due dates to tasks and show overdue tasks.
# 3. Add search functionality to find tasks by title or description.
# 4. Add statistics (total tasks, completed, pending).

