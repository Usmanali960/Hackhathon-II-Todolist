# Todo CLI - In-Memory Todo Application

**Hackathon II Phase I** - A command-line interface todo application with in-memory storage.

## Features

### Core Essentials (P1 - MVP)
- Create, update, delete, and view tasks
- Mark tasks as complete
- Unique task IDs

### Organization & Usability (P2)
- Priorities (high, medium, low)
- Tags/categories
- Search by keyword
- Filter by status, priority, due date
- Sort by due date, priority, title

### Advanced Features (P3)
- Due dates with overdue detection
- Time-based reminders
- Recurring tasks (daily, weekly, custom interval)

## Setup

### Prerequisites

- Python 3.13+
- UV package manager

### Installation

```bash
# Clone the repository
cd hackhathon-II-todolist

# Install dependencies (standard library only, UV for management)
uv sync
```

## Usage

### Run the application

```bash
# Menu-driven interface (default)
python -m src.cli.main

# Command-line interface
python -m src.cli.main add --help
```

### Basic Operations

```bash
# Add a task
python -m src.cli.main add --title "Buy groceries" --priority high

# View all tasks
python -m src.cli.main list

# Mark task as complete
python -m src.cli.main complete 1

# Delete a task
python -m src.cli.main delete 1
```

### Advanced Features

```bash
# Add task with due date and recurrence
python -m src.cli.main add \
    --title "Weekly meeting" \
    --due-date 2026-01-15 \
    --recurrence weekly \
    --tags work,important

# Search tasks
python -m src.cli.main search groceries

# Filter by priority
python -m src.cli.main filter --priority high

# Sort by due date
python -m src.cli.main sort --by due-date --order asc
```

## Documentation

For detailed usage instructions, see:
- **Quick Start Guide**: `specs/001-in-memory-todo-cli/quickstart.md`
- **Specification**: `specs/001-in-memory-todo-cli/spec.md`
- **Implementation Plan**: `specs/001-in-memory-todo-cli/plan.md`
- **Data Model**: `specs/001-in-memory-todo-cli/data-model.md`

## Architecture

```
src/
├── models/          # Domain entities (Task, enums)
├── services/         # Business logic (TaskStore, TaskOperations, RecurrenceEngine)
├── cli/             # CLI interface (commands, menu, formatter)
└── utils/           # Utilities (validators, datetime parser)
```

## Development

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run unit tests only
python -m unittest discover tests/unit/

# Run integration tests only
python -m unittest discover tests/integration/
```

## Phase I Scope

This is Phase I of a multi-phase project:
- **In-memory storage only** (no persistence)
- **No web UI or APIs**
- **No user authentication**
- **No AI integration**
- **No background services**

Future phases will add:
- Phase II: Web UI, database persistence, authentication
- Phase III: AI-powered chatbot interface
- Phase IV: Kubernetes deployment
- Phase V: Cloud-native event-driven architecture

## License

This project is part of the Hackathon II demonstration.
