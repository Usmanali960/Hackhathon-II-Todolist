"""Menu-driven CLI interface."""

from typing import Optional
from ..services.task_operations import TaskOperations
from .commands import CommandHandler
from .formatter import CLIFormatter


class MenuInterface:
    """Menu-driven CLI interface."""

    def __init__(self, operations: TaskOperations, formatter: CLIFormatter) -> None:
        """Initialize with operations, formatter, and command handler."""
        self._operations = operations
        self._formatter = formatter
        self._handler = CommandHandler(operations, formatter)

    def run(self) -> None:
        """Run main menu loop."""
        while True:
            self._display_main_menu()
            choice = input("Enter choice (1-6, q to quit): ").strip()

            if choice == "q":
                print("Goodbye!")
                break
            elif choice == "1":
                self._handle_add_task()
            elif choice == "2":
                self._handle_view_tasks()
            elif choice == "3":
                self._handle_complete_task()
            elif choice == "4":
                self._handle_update_task()
            elif choice == "5":
                self._handle_delete_task()
            elif choice == "6":
                self._handle_organization()
            else:
                print(self._formatter.format_error("Invalid choice. Please enter 1-6 or q."))

            input("\nPress Enter to continue...")

    def _display_main_menu(self) -> None:
        """Display main menu options."""
        print("\n" + "=" * 50)
        print("TODO CLI - MAIN MENU")
        print("=" * 50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Organization (Search, Filter, Sort)")
        print("q. Quit")
        print("=" * 50)

    def _handle_add_task(self) -> None:
        """Handle add task menu."""
        print("\n--- ADD TASK ---")

        title = input("Title: ").strip()
        if not title:
            print(self._formatter.format_error("Title is required."))
            return

        description = input("Description (optional): ").strip() or None
        priority = input("Priority [high/medium/low] (optional): ").strip().lower() or None
        tags = input("Tags (comma-separated, optional): ").strip() or None

        task = self._handler.handle_add(title, description, priority, tags)

        if task:
            print(self._formatter.format_success(f"Task #{task.id} created successfully."))
            print(self._formatter.format_task(task))
        else:
            print(self._formatter.format_error("Failed to create task."))

    def _handle_view_tasks(self) -> None:
        """Handle view tasks menu."""
        print("\n--- VIEW TASKS ---")
        tasks = self._handler.handle_list()

        print(self._formatter.format_list(tasks))

    def _handle_complete_task(self) -> None:
        """Handle mark task complete menu."""
        print("\n--- MARK TASK COMPLETE ---")
        task_id_str = input("Task ID: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print(self._formatter.format_error("Invalid task ID. Please enter a number."))
            return

        task = self._handler.handle_complete(task_id)

        if task:
            print(self._formatter.format_success(f"Task #{task.id} marked as complete."))
            print(self._formatter.format_task(task, show_details=True))
        else:
            print(self._formatter.format_error(f"Task #{task_id} not found."))

    def _handle_update_task(self) -> None:
        """Handle update task menu."""
        print("\n--- UPDATE TASK ---")
        task_id_str = input("Task ID: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print(self._formatter.format_error("Invalid task ID. Please enter a number."))
            return

        print("Leave blank to keep current value.")

        title = input("New title: ").strip() or None
        description = input("New description: ").strip() or None
        priority = input("New priority [high/medium/low]: ").strip().lower() or None
        tags = input("New tags (comma-separated): ").strip() or None

        task = self._handler.handle_update(task_id, title, description, priority, tags)

        if task:
            print(self._formatter.format_success(f"Task #{task.id} updated successfully."))
            print(self._formatter.format_task(task, show_details=True))
        else:
            print(self._formatter.format_error(f"Task #{task_id} not found."))

    def _handle_delete_task(self) -> None:
        """Handle delete task menu."""
        print("\n--- DELETE TASK ---")
        task_id_str = input("Task ID: ").strip()

        try:
            task_id = int(task_id_str)
        except ValueError:
            print(self._formatter.format_error("Invalid task ID. Please enter a number."))
            return

        # Show task before confirming - use the operations to get the specific task
        task_to_delete = self._operations.get_task(task_id)

        if task_to_delete:
            print("Task to delete:")
            print(self._formatter.format_task(task_to_delete, show_details=True))

            confirm = input("Delete this task? (y/n): ").strip().lower()

            if confirm == "y":
                result = self._handler.handle_delete(task_id)
                if result:
                    print(self._formatter.format_success(f"Task #{task_id} deleted successfully."))
                else:
                    print(self._formatter.format_error(f"Failed to delete task #{task_id}."))
            else:
                print("Delete cancelled.")
        else:
            print(self._formatter.format_error(f"Task #{task_id} not found."))

    def _handle_organization(self) -> None:
        """Handle organization menu (search, filter, sort)."""
        print("\n--- ORGANIZATION ---")
        print("1. Search Tasks")
        print("2. Filter Tasks")
        print("3. Sort Tasks")
        print("b. Back to Main Menu")

        choice = input("Enter choice (1-3, b): ").strip().lower()

        if choice == "1":
            self._handle_search_tasks()
        elif choice == "2":
            self._handle_filter_tasks()
        elif choice == "3":
            self._handle_sort_tasks()
        elif choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))

    def _handle_search_tasks(self) -> None:
        """Handle search tasks menu."""
        print("\n--- SEARCH TASKS ---")
        keyword = input("Search keyword: ").strip()

        if not keyword:
            print(self._formatter.format_error("Search keyword is required."))
            return

        tasks = self._handler.handle_search(keyword)

        criteria = f'keyword "{keyword}"'
        print(f"\n{self._formatter.format_filter_result(tasks, criteria)}")

        if tasks:
            for task in tasks:
                print(self._formatter.format_task(task))
        else:
            print(self._formatter.format_empty_list())

    def _handle_filter_tasks(self) -> None:
        """Handle filter tasks menu."""
        print("\n--- FILTER TASKS ---")
        print("1. By Status")
        print("2. By Priority")
        print("3. By Due Date")
        print("b. Back")

        choice = input("Enter choice (1-3, b): ").strip().lower()

        if choice == "1":
            self._filter_by_status()
        elif choice == "2":
            self._filter_by_priority()
        elif choice == "3":
            self._filter_by_due_date()
        elif choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))

    def _filter_by_status(self) -> None:
        """Filter tasks by status."""
        print("\nFilter by status:")
        print("1. Complete")
        print("2. Incomplete")
        print("b. Back")

        choice = input("Enter choice (1-2, b): ").strip().lower()

        if choice == "1":
            status = "complete"
        elif choice == "2":
            status = "incomplete"
        elif choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))
            return

        tasks = self._handler.handle_filter(status=status)

        criteria = f'status "{status}"'
        print(f"\n{self._formatter.format_filter_result(tasks, criteria)}")

        if tasks:
            for task in tasks:
                print(self._formatter.format_task(task))
        else:
            print(self._formatter.format_empty_list())

    def _filter_by_priority(self) -> None:
        """Filter tasks by priority."""
        print("\nFilter by priority:")
        print("1. High")
        print("2. Medium")
        print("3. Low")
        print("b. Back")

        choice = input("Enter choice (1-3, b): ").strip().lower()

        if choice == "1":
            priority = "high"
        elif choice == "2":
            priority = "medium"
        elif choice == "3":
            priority = "low"
        elif choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))
            return

        tasks = self._handler.handle_filter(priority=priority)

        criteria = f'priority "{priority}"'
        print(f"\n{self._formatter.format_filter_result(tasks, criteria)}")

        if tasks:
            for task in tasks:
                print(self._formatter.format_task(task))
        else:
            print(self._formatter.format_empty_list())

    def _filter_by_due_date(self) -> None:
        """Filter tasks by due date presence."""
        print("\nFilter by due date:")
        print("1. Has Due Date")
        print("2. No Due Date")
        print("b. Back")

        choice = input("Enter choice (1-2, b): ").strip().lower()

        if choice == "1":
            has_due_date = True
        elif choice == "2":
            has_due_date = False
        elif choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))
            return

        tasks = self._handler.handle_filter(has_due_date=has_due_date)

        print(f"\n{self._formatter.format_filter_result(tasks, 'has due date' if has_due_date else 'no due date')}")

        if tasks:
            for task in tasks:
                print(self._formatter.format_task(task))
        else:
            print(self._formatter.format_empty_list())

    def _handle_sort_tasks(self) -> None:
        """Handle sort tasks menu."""
        print("\n--- SORT TASKS ---")
        print("1. By Due Date")
        print("2. By Priority")
        print("3. By Title")
        print("b. Back")

        choice = input("Enter choice (1-3, b): ").strip().lower()

        if choice == "1":
            by = "due_date"
        elif choice == "2":
            by = "priority"
        elif choice == "3":
            by = "title"
        elif choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))
            return

        print("\nSort order:")
        print("1. Ascending")
        print("2. Descending")
        print("b. Back")

        order_choice = input("Enter choice (1-2, b): ").strip().lower()

        if order_choice == "1":
            order = "asc"
        elif order_choice == "2":
            order = "desc"
        elif order_choice == "b":
            return
        else:
            print(self._formatter.format_error("Invalid choice."))
            return

        tasks = self._handler.handle_sort(by, order)

        print(f"\nSorted by {by} ({order}ending):")

        if tasks:
            for task in tasks:
                print(self._formatter.format_task(task))
        else:
            print(self._formatter.format_empty_list())
