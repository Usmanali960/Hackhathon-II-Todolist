# Quick Start Guide: In-Memory Todo CLI Application

**Feature**: 001-in-memory-todo-cli | **Phase**: Phase I
**Purpose**: Setup and usage instructions for the in-memory Python CLI todo application.

---

## Prerequisites

- Python 3.13 or higher
- UV package manager
- Terminal/Command Line Interface

---

## Setup Instructions

### 1. Install UV (if not already installed)

```bash
# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# On Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Initialize Project

```bash
# Navigate to project directory
cd hackhathon-II-todolist

# Initialize UV environment (if not already done)
uv init

# Install dependencies (standard library only, but uv manages the project)
uv sync
```

### 3. Run the Application

```bash
# Run with menu interface (default)
python -m src.cli.main

# Or with command-line arguments
python -m src.cli.main add --help
```

---

## Basic Task Operations

### Add a Task

**Menu Interface**:
```
1. Add Task
Enter task title: Buy groceries
(Optional) Enter description: Get milk, eggs, and bread
(Optional) Enter priority [high/medium/low]: high
(Optional) Enter tags (comma-separated): shopping,urgent
```

**Command-Line Interface**:
```bash
# Minimal task
python -m src.cli.main add --title "Buy groceries"

# Task with all options
python -m src.cli.main add \
    --title "Buy groceries" \
    --description "Get milk, eggs, and bread" \
    --priority high \
    --tags shopping,urgent
```

### View All Tasks

**Menu Interface**:
```
2. View Tasks
```

**Command-Line Interface**:
```bash
python -m src.cli.main list
```

**Example Output**:
```
Tasks (3):
┌────┬─────────────────────────────┬────────┬──────┐
│ ID │ Title                       │ Status │ Prio │
├────┼─────────────────────────────┼────────┼──────┤
│  1 │ Buy groceries               │  ✗    │ HIGH │
│  2 │ Complete project docs       │  ✓    │ MED  │
│  3 │ Pay bills                  │  ✗    │ LOW  │
└────┴─────────────────────────────┴────────┴──────┘
```

### Update a Task

**Menu Interface**:
```
3. Update Task
Enter task ID: 1
Enter new title [keep blank to skip]: Buy groceries weekly
Enter new description: Weekly grocery shopping
Enter new priority [keep blank to skip]: medium
```

**Command-Line Interface**:
```bash
python -m src.cli.main update 1 --title "Buy groceries weekly" --priority medium
```

### Mark Task as Complete

**Menu Interface**:
```
4. Mark Complete
Enter task ID: 1
✓ Task #1 marked as complete.
Next occurrence generated: #4 Buy groceries (due tomorrow)
```

**Command-Line Interface**:
```bash
python -m src.cli.main complete 1
```

### Delete a Task

**Menu Interface**:
```
5. Delete Task
Enter task ID: 1
✓ Task #1 deleted.
```

**Command-Line Interface**:
```bash
python -m src.cli.main delete 1
```

---

## Organization & Usability Features

### Priorities

Assign priority when creating or updating tasks:
```
Priority values: high, medium, low
Default: medium
```

**Example**:
```bash
python -m src.cli.main add --title "Urgent task" --priority high
```

### Tags

Assign one or more tags to categorize tasks:
```
Tags are comma-separated values
Examples: work,personal,urgent
```

**Example**:
```bash
python -m src.cli.main add \
    --title "Meeting" \
    --tags work,important
```

### Search

Find tasks by keyword in title or description:

**Menu Interface**:
```
6. Search Tasks
Enter keyword: groceries
```

**Command-Line Interface**:
```bash
python -m src.cli.main search groceries
```

### Filter

Filter tasks by status, priority, or due date:

**Menu Interface**:
```
7. Filter Tasks
Filter by [status/priority/due_date]: priority
Filter value: high
```

**Command-Line Interface**:
```bash
# Filter by status
python -m src.cli.main filter --status incomplete

# Filter by priority
python -m src.cli.main filter --priority high

# Filter by due date
python -m src.cli.main filter --has-due-date
```

### Sort

Sort tasks by due date, priority, or title:

**Menu Interface**:
```
8. Sort Tasks
Sort by [due_date/priority/title]: due_date
Order [asc/desc]: asc
```

**Command-Line Interface**:
```bash
# Sort by due date (ascending)
python -m src.cli.main sort --by due_date --order asc

# Sort by priority (descending, default)
python -m src.cli.main sort --by priority

# Sort by title (alphabetical)
python -m src.cli.main sort --by title --order asc
```

### Combine Filter and Sort

Chain operations for advanced filtering:

**Command-Line Interface**:
```bash
# View incomplete high-priority tasks sorted by due date
python -m src.cli.main filter --status incomplete | \
    python -m src.cli.main filter --priority high | \
    python -m src.cli.main sort --by due_date
```

---

## Advanced Features

### Due Dates

Assign due dates to tasks:

**Menu Interface**:
```
1. Add Task
Enter task title: Submit report
(Optional) Enter due date [YYYY-MM-DD or MM/DD/YYYY]: 2026-01-15
```

**Command-Line Interface**:
```bash
# YYYY-MM-DD format
python -m src.cli.main add --title "Submit report" --due-date 2026-01-15

# MM/DD/YYYY format
python -m src.cli.main add --title "Submit report" --due-date 01/15/2026
```

**Overdue Indicator**: Tasks with due dates in the past display with ⚠ symbol:
```
[⚠] #1: Submit report (OVERDUE)
```

### Reminders

Set reminder times to get notified when tasks are due:

**Menu Interface**:
```
1. Add Task
Enter task title: Attend meeting
(Optional) Enter due date [YYYY-MM-DD]: 2026-01-15
(Optional) Enter reminder time [HH:MM or HH:MM AM/PM]: 09:00
```

**Command-Line Interface**:
```bash
python -m src.cli.main add \
    --title "Attend meeting" \
    --due-date 2026-01-15 \
    --reminder-time "09:00"
```

**Reminder Notifications**:
- Reminders trigger during application runtime
- System checks for due reminders every 5 seconds
- Notification displays when reminder time is reached:
  ```
  🔔 REMINDER: Task #1 "Attend meeting" is due now!
  ```

### Recurring Tasks

Create tasks that repeat daily, weekly, or on custom intervals:

**Menu Interface**:
```
1. Add Task
Enter task title: Weekly team meeting
(Optional) Enter due date: 2026-01-08
(Optional) Enter recurrence rule [daily/weekly/custom]: weekly
(Optional) Enter interval (for custom, in days): [blank]
```

**Command-Line Interface**:
```bash
# Daily recurring task
python -m src.cli.main add \
    --title "Daily standup" \
    --due-date 2026-01-01 \
    --recurrence daily

# Weekly recurring task
python -m src.cli.main add \
    --title "Weekly team meeting" \
    --due-date 2026-01-08 \
    --recurrence weekly

# Custom interval (every 3 days)
python -m src.cli.main add \
    --title "Water plants" \
    --due-date 2026-01-01 \
    --recurrence custom --interval 3
```

**Recurring Task Behavior**:
- When you mark a recurring task as complete, a new task is automatically generated
- The new task has the same title, description, priority, and tags
- The due date is shifted forward by the recurrence interval
- Example: If you complete a weekly task due on 2026-01-08, next task is due 2026-01-15

---

## Complete Workflow Example

### Scenario: Manage a Project Task List

**Step 1: Create Initial Tasks**
```bash
python -m src.cli.main add \
    --title "Complete project documentation" \
    --description "Finish all markdown files" \
    --priority high \
    --tags work,documentation \
    --due-date 2026-01-15 \
    --recurrence weekly

python -m src.cli.main add \
    --title "Review pull requests" \
    --priority medium \
    --tags work,review

python -m src.cli.main add \
    --title "Buy coffee" \
    --priority low \
    --tags personal
```

**Step 2: View All Tasks**
```bash
python -m src.cli.main list
```

**Step 3: Search for Work Tasks**
```bash
python -m src.cli.main search work
```

**Step 4: Filter High Priority Tasks**
```bash
python -m src.cli.main filter --priority high
```

**Step 5: Mark Task as Complete**
```bash
python -m src.cli.main complete 1
# Output: ✓ Task #1 marked as complete.
#         Next occurrence generated: #4 Complete project documentation (due 2026-01-22)
```

**Step 6: View Updated List**
```bash
python -m src.cli.main list
```

**Step 7: Sort by Due Date**
```bash
python -m src.cli.main sort --by due_date
```

---

## Important Notes

### Data Persistence

- **In-Memory Only**: Tasks are stored in memory and lost when the application exits
- **No Database**: Phase I does not support file or database persistence
- **Future Phases**: Phase II will add database persistence and web UI

### Reminder Notifications

- **Runtime Only**: Reminders only trigger while the application is running
- **Polling**: System checks for reminders every 5 seconds during idle time
- **Notification Format**: Reminders display as CLI notifications, not system notifications

### Recurring Tasks

- **On Completion**: Next occurrence generates only when current task is marked complete
- **ID Generation**: Each occurrence gets a unique auto-incrementing ID
- **Attribute Preservation**: Title, description, priority, and tags are copied to next occurrence

### Error Handling

- **Clear Messages**: All errors display with descriptive messages and suggestions
- **Graceful Degradation**: System never crashes; always returns to menu or prompt
- **Validation**: Inputs are validated before execution

---

## Common Issues and Solutions

### Issue: "Invalid date format"

**Problem**: Due date or reminder time not in recognized format.

**Solution**: Use one of these formats:
- `YYYY-MM-DD` (recommended): `2026-01-15`
- `MM/DD/YYYY`: `01/15/2026`
- Reminder times: `09:00` or `09:00 AM`

### Issue: "Reminder time must be before or at due date"

**Problem**: Reminder time is after the due date.

**Solution**: Set reminder time before or at the due date time.

### Issue: "Task #999 not found"

**Problem**: Task ID does not exist.

**Solution**: Use `list` command to see available task IDs.

### Issue: "No tasks found"

**Problem**: Task list is empty or filter matches no tasks.

**Solution**: Create tasks using `add` command, or adjust filter criteria.

---

## Help and Documentation

### Command-Line Help

Get help for any command:

```bash
# General help
python -m src.cli.main --help

# Command-specific help
python -m src.cli.main add --help
python -m src.cli.main filter --help
python -m src.cli.main sort --help
```

### Available Commands

```bash
add        - Create a new task
list        - View all tasks
delete      - Delete a task by ID
update      - Update a task by ID
complete    - Mark a task as complete
search      - Search tasks by keyword
filter      - Filter tasks by criteria
sort        - Sort tasks by criteria
help        - Display help information
```

---

## Next Steps

After familiarizing yourself with the CLI interface:

1. **Explore Advanced Features**: Try recurring tasks and reminders
2. **Test Edge Cases**: Create tasks with various attributes and test filter/sort combinations
3. **Prepare for Phase II**: Understand the data model for future database integration
4. **Read the Specification**: Refer to `specs/001-in-memory-todo-cli/spec.md` for complete requirements

---

## Support

For issues or questions:
1. Check this quickstart guide for common solutions
2. Review the specification at `specs/001-in-memory-todo-cli/spec.md`
3. Review the data model at `specs/001-in-memory-todo-cli/data-model.md`
4. Check command-line help with `--help` flag

---

**Phase I Complete**: This application serves as the foundation for future phases including database persistence (Phase II), AI-powered chatbot interface (Phase III), Kubernetes deployment (Phase IV), and cloud-native event-driven architecture (Phase V).
