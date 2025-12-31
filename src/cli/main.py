"""Main CLI entry point."""

import sys
import argparse
from ..services.task_store import TaskStore
from ..services.task_operations import TaskOperations
from .formatter import CLIFormatter
from .menu import MenuInterface


def main() -> None:
    """Main entry point for CLI application."""
    # Initialize components
    store = TaskStore()
    operations = TaskOperations(store)
    formatter = CLIFormatter()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Todo CLI - In-memory todo application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["add", "list", "delete", "update", "complete", "search", "filter", "sort"],
        help="Command to execute",
    )

    # Add command arguments
    # Add command
    parser.add_argument(
        "--title",
        help="Task title (required for add command)",
    )
    parser.add_argument(
        "--description",
        help="Task description",
    )
    parser.add_argument(
        "--priority",
        choices=["high", "medium", "low"],
        help="Task priority",
    )
    parser.add_argument(
        "--tags",
        help="Comma-separated tags",
    )
    parser.add_argument(
        "--id",
        type=int,
        help="Task ID (required for delete, update, complete commands)",
    )

    # Search command arguments
    parser.add_argument(
        "--keyword",
        help="Search keyword",
    )

    # Filter command arguments
    parser.add_argument(
        "--status",
        choices=["complete", "incomplete"],
        help="Filter by status",
    )
    parser.add_argument(
        "--has-due-date",
        action="store_true",
        help="Filter tasks with due dates only",
    )

    # Sort command arguments
    parser.add_argument(
        "--by",
        choices=["due_date", "priority", "title"],
        help="Sort by field",
    )
    parser.add_argument(
        "--order",
        choices=["asc", "desc"],
        default="asc",
        help="Sort order (asc/desc)",
    )

    args = parser.parse_args()

    # If no command, run menu interface
    if not args.command:
        menu = MenuInterface(operations, formatter)
        menu.run()
        return

    # Execute command
    try:
        if args.command == "add":
            handle_add_command(args, operations, formatter)
        elif args.command == "list":
            handle_list_command(operations, formatter)
        elif args.command == "delete":
            handle_delete_command(args, operations, formatter)
        elif args.command == "update":
            handle_update_command(args, operations, formatter)
        elif args.command == "complete":
            handle_complete_command(args, operations, formatter)
        elif args.command == "search":
            handle_search_command(args, operations, formatter)
        elif args.command == "filter":
            handle_filter_command(args, operations, formatter)
        elif args.command == "sort":
            handle_sort_command(args, operations, formatter)
    except Exception as e:
        print(formatter.format_error(str(e)))
        sys.exit(1)


def handle_add_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle add command."""
    from .commands import CommandHandler

    handler = CommandHandler(operations, formatter)

    if not args.title:
        print(formatter.format_error("--title is required for add command"))
        sys.exit(1)

    task = handler.handle_add(
        args.title,
        args.description,
        args.priority,
        args.tags,
    )

    if task:
        print(formatter.format_success(f"Task #{task.id} created successfully."))
        print(formatter.format_task(task))
    else:
        print(formatter.format_error("Failed to create task"))
        sys.exit(1)


def handle_list_command(operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle list command."""
    from .commands import CommandHandler

    handler = CommandHandler(operations, formatter)
    tasks = handler.handle_list()

    print(formatter.format_list(tasks))


def handle_delete_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle delete command."""
    from .commands import CommandHandler

    if not args.id:
        print(formatter.format_error("--id is required for delete command"))
        sys.exit(1)

    handler = CommandHandler(operations, formatter)
    result = handler.handle_delete(args.id)

    if result:
        print(formatter.format_success(f"Task #{args.id} deleted successfully."))
    else:
        print(formatter.format_error(f"Task #{args.id} not found"))
        sys.exit(1)


def handle_update_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle update command."""
    from .commands import CommandHandler

    if not args.id:
        print(formatter.format_error("--id is required for update command"))
        sys.exit(1)

    handler = CommandHandler(operations, formatter)
    task = handler.handle_update(
        args.id,
        args.title,
        args.description,
        args.priority,
        args.tags,
    )

    if task:
        print(formatter.format_success(f"Task #{task.id} updated successfully."))
        print(formatter.format_task(task, show_details=True))
    else:
        print(formatter.format_error(f"Task #{args.id} not found"))
        sys.exit(1)


def handle_complete_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle complete command."""
    from .commands import CommandHandler

    if not args.id:
        print(formatter.format_error("--id is required for complete command"))
        sys.exit(1)

    handler = CommandHandler(operations, formatter)
    task = handler.handle_complete(args.id)

    if task:
        print(formatter.format_success(f"Task #{task.id} marked as complete."))
        print(formatter.format_task(task, show_details=True))
    else:
        print(formatter.format_error(f"Task #{args.id} not found"))
        sys.exit(1)


def handle_search_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle search command."""
    from .commands import CommandHandler

    if not args.keyword:
        print(formatter.format_error("--keyword is required for search command"))
        sys.exit(1)

    handler = CommandHandler(operations, formatter)
    tasks = handler.handle_search(args.keyword)

    print(formatter.format_filter_result(tasks, f'keyword "{args.keyword}"'))

    if tasks:
        for task in tasks:
            print(formatter.format_task(task))
    else:
        print(formatter.format_empty_list())


def handle_filter_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle filter command."""
    from .commands import CommandHandler

    handler = CommandHandler(operations, formatter)
    tasks = handler.handle_filter(args.status, args.priority, args.has_due_date)

    if args.status:
        criteria = f'status "{args.status}"'
    elif args.priority:
        criteria = f'priority "{args.priority}"'
    elif args.has_due_date:
        criteria = "has due date"
    else:
        criteria = "all tasks"

    print(formatter.format_filter_result(tasks, criteria))

    if tasks:
        for task in tasks:
            print(formatter.format_task(task))
    else:
        print(formatter.format_empty_list())


def handle_sort_command(args, operations: TaskOperations, formatter: CLIFormatter) -> None:
    """Handle sort command."""
    from .commands import CommandHandler

    if not args.by:
        print(formatter.format_error("--by is required for sort command"))
        sys.exit(1)

    handler = CommandHandler(operations, formatter)
    tasks = handler.handle_sort(args.by, args.order)

    print(f"Sorted by {args.by} ({args.order}ending):")

    if tasks:
        for task in tasks:
            print(formatter.format_task(task))
    else:
        print(formatter.format_empty_list())


if __name__ == "__main__":
    main()
