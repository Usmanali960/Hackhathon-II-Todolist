# Architecture Contracts: Task Operations

**Feature**: 001-in-memory-todo-cli | **Plan Reference**: plan.md (Phase 1.2)
**Purpose**: Define internal API boundaries between modules for independent testing and future refactoring.

---

## Contract: TaskStore

**Module**: `src/services/task_store.py`
**Purpose**: In-memory storage and retrieval of Task entities

### Interface

```python
class TaskStore:
    """In-memory storage for Task entities."""

    def __init__(self) -> None:
        """Initialize empty task store with auto-incrementing ID counter."""
        ...

    def add(self, task: Task) -> Task:
        """
        Add task to storage and assign auto-incrementing ID.

        Args:
            task: Task entity without ID (id will be assigned)

        Returns:
            Task with assigned ID

        Raises:
            ValueError: If task validation fails
        """
        ...

    def get(self, id: int) -> Task | None:
        """
        Retrieve task by ID.

        Args:
            id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        ...

    def delete(self, id: int) -> bool:
        """
        Delete task by ID.

        Args:
            id: Task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        ...

    def update(self, id: int, **fields) -> Task | None:
        """
        Update task fields by ID.

        Args:
            id: Task ID to update
            **fields: Fields to update (title, description, priority, tags, etc.)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If validation fails for any field
        """
        ...

    def list_all(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all Task entities (empty list if none exist)
        """
        ...

    def exists(self, id: int) -> bool:
        """
        Check if task exists.

        Args:
            id: Task ID to check

        Returns:
            True if task exists, False otherwise
        """
        ...

    def count(self) -> int:
        """
        Get total task count.

        Returns:
            Number of tasks in storage
        """
        ...
```

### Implementation Notes

- **Storage**: Use dict[int, Task] for O(1) lookups by ID
- **ID Generation**: Counter starts at 1, increments on each add()
- **Immutability**: Tasks are stored as-is; updates create new objects
- **Thread Safety**: Not required (single-threaded CLI application)

---

## Contract: TaskOperations

**Module**: `src/services/task_operations.py`
**Purpose**: Business logic for CRUD, search, filter, sort, and recurrence

### Interface

```python
class TaskOperations:
    """Business logic for task operations."""

    def __init__(self, store: TaskStore) -> None:
        """Initialize with task store dependency."""
        ...

    def create_task(
        self,
        title: str,
        description: str | None = None,
        priority: Priority = Priority.MEDIUM,
        tags: Set[str] | None = None,
        due_date: datetime | None = None,
        reminder_time: datetime | None = None,
        recurrence_rule: RecurrenceRule | None = None,
    ) -> Task:
        """
        Create new task with validation.

        Args:
            title: Task title (required)
            description: Optional description
            priority: Task priority (default: MEDIUM)
            tags: Set of tags (default: empty)
            due_date: Optional due date
            reminder_time: Optional reminder time
            recurrence_rule: Optional recurrence rule

        Returns:
            Created Task with auto-generated ID

        Raises:
            ValueError: If validation fails
        """
        ...

    def delete_task(self, id: int) -> bool:
        """
        Delete task by ID.

        Args:
            id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        ...

    def update_task(self, id: int, **fields) -> Task | None:
        """
        Update task fields by ID.

        Args:
            id: Task ID to update
            **fields: Fields to update (any Task attribute except id/created_at)

        Returns:
            Updated Task if found, None otherwise

        Raises:
            ValueError: If validation fails or trying to update immutable fields
        """
        ...

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all Task entities
        """
        ...

    def toggle_complete(self, id: int) -> Task | None:
        """
        Toggle task completion status and generate recurring task if applicable.

        Args:
            id: Task ID to toggle

        Returns:
            Updated Task if found, None otherwise

        Note:
            If task has recurrence_rule, generates next occurrence task
        """
        ...

    def search_tasks(self, keyword: str) -> list[Task]:
        """
        Search tasks by keyword in title or description.

        Args:
            keyword: Search term (case-insensitive)

        Returns:
            List of matching Tasks (empty if none match)
        """
        ...

    def filter_by_status(self, status: Status) -> list[Task]:
        """
        Filter tasks by completion status.

        Args:
            status: Status to filter by

        Returns:
            List of matching Tasks
        """
        ...

    def filter_by_priority(self, priority: Priority) -> list[Task]:
        """
        Filter tasks by priority level.

        Args:
            priority: Priority to filter by

        Returns:
            List of matching Tasks
        """
        ...

    def filter_by_due_date(self, has_due_date: bool) -> list[Task]:
        """
        Filter tasks by presence of due date.

        Args:
            has_due_date: True to include only tasks with due dates,
                        False to include only tasks without due dates

        Returns:
            List of matching Tasks
        """
        ...

    def sort_by_due_date(self, ascending: bool = True) -> list[Task]:
        """
        Sort tasks by due date.

        Args:
            ascending: Sort order (default: ascending)

        Returns:
            Sorted list of Tasks (tasks without due_date placed at end)

        Note:
            Tasks without due_date are placed after tasks with due_date
        """
        ...

    def sort_by_priority(self, ascending: bool = False) -> list[Task]:
        """
        Sort tasks by priority (HIGH > MEDIUM > LOW).

        Args:
            ascending: Sort order (default: descending)

        Returns:
            Sorted list of Tasks

        Note:
            Priority order: HIGH > MEDIUM > LOW
        """
        ...

    def sort_by_title(self, ascending: bool = True) -> list[Task]:
        """
        Sort tasks alphabetically by title.

        Args:
            ascending: Sort order (default: ascending)

        Returns:
            Sorted list of Tasks (case-insensitive)
        """
        ...

    def get_overdue_tasks(self) -> list[Task]:
        """
        Get all overdue tasks.

        Returns:
            List of Tasks that are overdue (due_date < now AND status INCOMPLETE)
        """
        ...

    def get_due_reminders(self) -> list[Task]:
        """
        Get tasks with due reminders.

        Returns:
            List of Tasks with reminder_time <= now AND reminder_notified == False
        """
        ...

    def mark_reminder_notified(self, task: Task) -> None:
        """
        Mark task reminder as notified.

        Args:
            task: Task to update

        Note:
            Updates task in storage with reminder_notified = True
        """
        ...
```

### Implementation Notes

- **Validation**: All methods validate inputs before delegating to TaskStore
- **Business Logic**: Search, filter, and sort operate on TaskStore.list_all() results
- **Recurrence Integration**: toggle_complete() integrates with RecurrenceEngine
- **Chaining**: Filter and sort methods can be chained by passing list results

---

## Contract: RecurrenceEngine

**Module**: `src/services/recurrence_engine.py`
**Purpose**: Calculate next occurrence for recurring tasks

### Interface

```python
class RecurrenceEngine:
    """Calculate next occurrence of recurring tasks."""

    def calculate_next_occurrence(self, current_task: Task) -> Task:
        """
        Calculate next occurrence task based on recurrence rule.

        Args:
            current_task: Completed task with recurrence_rule

        Returns:
            New Task for next occurrence with:
            - New ID (auto-assigned when added to store)
            - Same title, description, priority, tags
            - Updated due_date based on recurrence rule
            - Updated reminder_time (shifted by same interval)
            - Same recurrence_rule
            - status INCOMPLETE
            - reminder_notified False

        Raises:
            ValueError: If recurrence_rule is invalid or interval missing for CUSTOM type

        Note:
            Caller is responsible for adding returned Task to TaskStore
        """
        ...

    def calculate_next_due_date(
        self,
        current_due_date: datetime,
        recurrence_rule: RecurrenceRule
    ) -> datetime:
        """
        Calculate next due date based on recurrence rule.

        Args:
            current_due_date: Current task's due date
            recurrence_rule: Recurrence rule to apply

        Returns:
            Next due date datetime

        Raises:
            ValueError: If recurrence_rule is invalid
        """
        ...

    def calculate_next_reminder_time(
        self,
        current_reminder_time: datetime,
        current_due_date: datetime,
        next_due_date: datetime
    ) -> datetime:
        """
        Calculate next reminder time based on recurrence interval.

        Args:
            current_reminder_time: Current task's reminder time
            current_due_date: Current task's due date
            next_due_date: Next task's due date

        Returns:
            Next reminder time (shifted by same interval as due_date)

        Note:
            Preserves the time offset between reminder and due date
        """
        ...
```

### Implementation Notes

- **DAILY**: Increment due date by 1 day
- **WEEKLY**: Increment due date by 7 days
- **CUSTOM**: Increment due date by `recurrence_rule.interval_days` days
- **Reminder Preservation**: Reminder time shifted by same interval to maintain offset from due date
- **Attribute Preservation**: Title, description, priority, tags copied; status reset to INCOMPLETE

---

## Contract: CLIFormatter

**Module**: `src/cli/formatter.py`
**Purpose**: Format output for consistent CLI display

### Interface

```python
class CLIFormatter:
    """Format output for CLI display."""

    def format_task(self, task: Task, show_details: bool = False) -> str:
        """
        Format single task for display.

        Args:
            task: Task to format
            show_details: If True, include all attributes; if False, summary only

        Returns:
            Formatted string for CLI display

        Example (summary):
            [✗] #1: Buy groceries (MEDIUM)

        Example (detailed):
            [✗] #1: Buy groceries (MEDIUM)
                Due: 2025-01-15 | Tags: shopping, urgent
                Description: Buy milk, eggs, and bread
        """
        ...

    def format_list(self, tasks: list[Task]) -> str:
        """
        Format list of tasks for display.

        Args:
            tasks: List of Tasks to format

        Returns:
            Formatted string with task list header and table

        Example:
            Tasks (3):
            ┌────┬─────────────────────────────┬────────┬──────┐
            │ ID │ Title                       │ Status │ Prio │
            ├────┼─────────────────────────────┼────────┼──────┤
            │  1 │ Buy groceries               │  ✗    │ MED  │
            │  2 │ Complete project docs       │  ✓    │ HIGH │
            │  3 │ ✗ #3: Pay bills (OVERDUE) │  ✗    │ LOW  │
            └────┴─────────────────────────────┴────────┴──────┘
        """
        ...

    def format_error(self, message: str) -> str:
        """
        Format error message for display.

        Args:
            message: Error message

        Returns:
            Formatted error string with consistent prefix

        Example:
            ERROR: Task #999 not found.
        """
        ...

    def format_reminder(self, task: Task) -> str:
        """
        Format reminder notification for display.

        Args:
            task: Task with due reminder

        Returns:
            Formatted reminder string for CLI notification

        Example:
            🔔 REMINDER: Task #1 "Buy groceries" is due now!
        """
        ...

    def format_success(self, message: str) -> str:
        """
        Format success message for display.

        Args:
            message: Success message

        Returns:
            Formatted success string

        Example:
            ✓ Task created successfully.
        """
        ...

    def format_empty_list(self) -> str:
        """
        Format message for empty task list.

        Returns:
            Formatted message for no tasks

        Example:
            No tasks found. Use 'Add Task' to create your first task.
        """
        ...

    def format_filter_result(self, tasks: list[Task], criteria: str) -> str:
        """
        Format filter result message.

        Args:
            tasks: Filtered task list
            criteria: Description of filter criteria

        Returns:
            Formatted result message with count

        Example:
            Found 2 tasks matching "high" priority:
            ...
        """
        ...
```

### Visual Indicators

| Symbol | Meaning |
|---------|----------|
| ✓ | Complete task |
| ✗ | Incomplete task |
| ⚠ | Overdue task |
| 🔔 | Reminder notification |
| ❌ | Error |
| ✓ | Success |

---

## Module Dependency Graph

```
CLI Module (cli/)
├── TaskOperations (services/task_operations.py)
│   ├── TaskStore (services/task_store.py)
│   ├── RecurrenceEngine (services/recurrence_engine.py)
│   └── Task (models/task.py)
├── CLIFormatter (cli/formatter.py)
│   └── Task (models/task.py)
└── Validators (utils/validators.py)
    └── Task (models/task.py)
```

---

## Testing Strategy

Each contract has corresponding test file:

- `tests/unit/test_task_store.py` - TaskStore contract tests
- `tests/unit/test_task_operations.py` - TaskOperations contract tests
- `tests/unit/test_recurrence_engine.py` - RecurrenceEngine contract tests
- `tests/unit/test_formatter.py` - CLIFormatter contract tests

Tests validate:
- Interface compliance (methods exist with correct signatures)
- Input validation and error handling
- Return type correctness
- Edge case handling (empty lists, invalid IDs, etc.)

---

## Future Extensibility (Phase II+)

These contracts are designed to support future phases:

1. **TaskStore Persistence**: Replace in-memory dict with database adapter (Phase II)
2. **TaskOperations Multi-User**: Add user_id filtering (Phase II)
3. **CLIFormatter Web**: Replace with HTML/JSON formatters (Phase II)
4. **MCP Tool Wrapping**: Expose TaskOperations methods as MCP tools (Phase III)

Contract interfaces remain stable; only implementations change.
