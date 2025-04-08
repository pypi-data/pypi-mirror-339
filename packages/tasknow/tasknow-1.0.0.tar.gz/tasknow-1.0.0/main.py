"""TaskNow - A minimalist terminal task manager."""
import argparse
import json
import os
from typing import List, Dict, Optional

TASKS_FILE = "tasks.json"

class TaskManager:
    """Manages tasks storage and operations."""
    
    def __init__(self) -> None:
        """Initialize task manager and load tasks."""
        self.tasks: List[Dict] = []
        self.current_task_id: Optional[int] = None
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from JSON file or create new file if doesn't exist."""
        try:
            if os.path.exists(TASKS_FILE):
                with open(TASKS_FILE, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
                    self.current_task_id = data.get('current_task_id')
                    # If no current task but incomplete tasks exist, set first one
                    if self.current_task_id is None and self.tasks:
                        first_incomplete = next(
                            (t for t in self.tasks if not t['completed']),
                            None
                        )
                        if first_incomplete:
                            self.current_task_id = first_incomplete['id']
            else:
                self._save_tasks()
        except json.JSONDecodeError:
            print("Error: Corrupted tasks file. Starting with empty task list.")
            self.tasks = []
            self.current_task_id = None
            self._save_tasks()

    def _save_tasks(self) -> None:
        """Save tasks to JSON file."""
        with open(TASKS_FILE, 'w') as f:
            json.dump({
                'tasks': self.tasks,
                'current_task_id': self.current_task_id
            }, f, indent=2)

    def add_task(self, description: str) -> None:
        """Add a new task with auto-incrementing ID."""
        new_id = max((task['id'] for task in self.tasks), default=0) + 1
        self.tasks.append({
            'id': new_id,
            'description': description,
            'completed': False
        })
        if self.current_task_id is None:
            self.current_task_id = new_id
        self._save_tasks()

    def complete_current_task(self) -> None:
        """Mark current task as completed."""
        if self.current_task_id is None:
            print("No current task to complete")
            return
            
        for task in self.tasks:
            if task['id'] == self.current_task_id:
                task_description = task['description']
                task['completed'] = True
                # Find next incomplete task if available
                next_task = next(
                    (t for t in self.tasks if not t['completed'] and t['id'] != self.current_task_id),
                    None
                )
                self.current_task_id = next_task['id'] if next_task else None
                self._save_tasks()
                print(f"Completed task: {task_description}")
                return
        print("Error: Current task not found")

    def edit_task(self, task_id: int, new_description: str) -> None:
        """Edit a task's description."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                self._save_tasks()
                return
        print(f"Error: Task {task_id} not found")

    def get_current_task(self) -> Optional[Dict]:
        """Get current active task (always earliest incomplete)."""
        incomplete = sorted(
            [t for t in self.tasks if not t['completed']],
            key=lambda x: x['id']
        )
        
        if not incomplete:
            self.current_task_id = None
            self._save_tasks()
            return None
            
        # Always use earliest incomplete task
        if self.current_task_id != incomplete[0]['id']:
            self.current_task_id = incomplete[0]['id']
            self._save_tasks()
            
        return next(
            (t for t in self.tasks if t['id'] == self.current_task_id),
            None
        )

    def list_tasks(self) -> List[Dict]:
        """Get all incomplete tasks."""
        return [task for task in self.tasks if not task['completed']]

    def remove_task(self, task_id: int) -> None:
        """Remove a task by ID."""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                if self.current_task_id == task_id:
                    # Find next incomplete task if available
                    next_task = next(
                        (t for t in self.tasks
                         if not t['completed'] and t['id'] != task_id),
                        None
                    )
                    self.current_task_id = next_task['id'] if next_task else None
                del self.tasks[i]
                self._save_tasks()
                return
        print(f"Error: Task {task_id} not found")

    def list_completed_tasks(self) -> List[Dict]:
        """Get all completed tasks."""
        return [task for task in self.tasks if task['completed']]

    def reopen_task(self, task_id: int) -> None:
        """Reopen a completed task and make it current."""
        for task in self.tasks:
            if task['id'] == task_id:
                if not task['completed']:
                    print(f"Error: Task {task_id} is not completed")
                    return
                task['completed'] = False
                self.current_task_id = task_id
                self._save_tasks()
                return
        print(f"Error: Task {task_id} not found")

def main() -> None:
    """Handle CLI commands and execute appropriate actions."""
    parser = argparse.ArgumentParser(
        description='TaskNow - Minimalist Task Manager',
        epilog='If no command is provided, defaults to showing the current task.'
    )
    subparsers = parser.add_subparsers(dest='command')

    # Show current task
    subparsers.add_parser('show', help='Show current task')

    # Add new task
    add_parser = subparsers.add_parser('add', help='Add a new task (requires description)')
    add_parser.add_argument('description', nargs='*', help='Task description (no quotes needed)')

    # Complete current task
    subparsers.add_parser('done', help='Mark current task as done (no arguments)')

    # List all tasks
    subparsers.add_parser('list', help='List all tasks (no arguments)')

    # List completed tasks
    subparsers.add_parser('completed', help='List completed tasks (no arguments)')

    # Remove task
    remove_parser = subparsers.add_parser('remove', help='Remove a task (requires ID)')
    remove_parser.add_argument('id', type=int, help='Task ID to remove')

    # Mark task as undone
    undone_parser = subparsers.add_parser('undone', help='Mark a completed task as undone (requires ID)')
    undone_parser.add_argument('id', type=int, help='Task ID to mark as undone')

    # Edit task
    edit_parser = subparsers.add_parser('edit', help='Edit a task description (requires ID and new description)')
    edit_parser.add_argument('id', type=int, help='Task ID to edit')
    edit_parser.add_argument('new_description', nargs='*', help='New task description')

    args = parser.parse_args()
    if args.command is None:
        args.command = 'show'
    manager = TaskManager()

    try:
        if args.command == 'show':
            current = manager.get_current_task()
            if current:
                print(f"Current task: {current['description']}")
            else:
                print("No current task")

        elif args.command == 'add':
            description = ' '.join(args.description)
            manager.add_task(description)
            print(f"Added task: {description}")

        elif args.command == 'edit':
            new_desc = ' '.join(args.new_description)
            manager.edit_task(args.id, new_desc)
            print(f"Updated task {args.id}")

        elif args.command == 'done':
            manager.complete_current_task()

        elif args.command == 'list':
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks")
            else:
                for task in tasks:
                    status = "✓" if task['completed'] else " "
                    print(f"{task['id']}. [{status}] {task['description']}")

        elif args.command == 'completed':
            tasks = manager.list_completed_tasks()
            if not tasks:
                print("No completed tasks")
            else:
                for task in tasks:
                    print(f"{task['id']}. {task['description']}")

        elif args.command == 'remove':
            manager.remove_task(args.id)
            print(f"Removed task {args.id}")

        elif args.command == 'undone':
            manager.reopen_task(args.id)
            print(f"Marked task {args.id} as undone")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()