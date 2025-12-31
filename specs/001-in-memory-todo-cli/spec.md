# Feature Specification: Hackathon II Phase I - In-Memory Todo Application (CLI)

**Feature Branch**: `001-in-memory-todo-cli`
**Created**: 2025-12-31
**Status**: Draft
**Input**: Hackathon II Phase I: In-Memory Todo Application (CLI)

## Scope

This specification applies **ONLY** to Phase I.

- Application type: CLI (Command Line Interface)
- Data storage: In-memory only (no database, no files)
- Persistence across restarts: NOT required
- Network, web, AI, authentication, cloud: NOT allowed in Phase I

All future phases will build on this spec.

## Non-Goals (Explicit Exclusions)

The following are **strictly out of scope** for Phase I:

- Web UI or APIs
- Databases or file persistence
- User authentication or accounts
- AI agents or MCP tools
- Background services or schedulers
- Cloud or containerization

## User Scenarios & Testing

### User Story 1 - Basic Task Management (Priority: P1)

A user launches the todo application and performs essential task operations: adding tasks, viewing all tasks, marking tasks as complete, and deleting tasks. The user can also update any task details when information changes.

**Why this priority**: This is the core foundation of any todo application. Without these basic operations, the application provides no value to users. All other features build upon this foundation.

**Independent Test**: Can be fully tested by creating a task, viewing it, marking it complete, and deleting it. This delivers immediate value by allowing users to track and manage simple task lists.

**Acceptance Scenarios**:

1. **Given** the application starts with an empty task list, **When** a user adds a task with a title, **Then** the task appears in the list with a unique ID
2. **Given** a task exists in the list, **When** the user views all tasks, **Then** all tasks display in a readable format with key attributes (ID, title, status, priority)
3. **Given** an incomplete task exists, **When** the user marks it as complete, **Then** the task status updates to complete
4. **Given** a task exists, **When** the user deletes it by ID, **Then** the task is removed from the list and no longer appears in future views
5. **Given** a task exists, **When** the user updates the title, **Then** the task reflects the new title in all displays
6. **Given** the user provides an invalid task ID for deletion, **When** the delete operation is attempted, **Then** the system displays a clear error message indicating the task was not found

---

### User Story 2 - Task Organization (Priority: P2)

A user organizes their tasks by assigning priorities (high/medium/low) and categories (tags), then filters and sorts tasks to find what they need quickly. They can also search for tasks by keyword in titles or descriptions.

**Why this priority**: As task lists grow, organization becomes essential for productivity. This feature enables users to prioritize work and find tasks efficiently without scanning through large unsorted lists.

**Independent Test**: Can be tested by creating multiple tasks with different priorities and tags, then filtering by a specific priority and sorting by due date. Delivers value by reducing time spent locating relevant tasks.

**Acceptance Scenarios**:

1. **Given** a task is being created, **When** the user specifies a priority (high/medium/low), **Then** the task stores and displays the priority
2. **Given** a task is being created or updated, **When** the user assigns one or more tags, **Then** the task associates with all specified tags
3. **Given** multiple tasks exist with different priorities, **When** the user filters by priority "high", **Then** only high-priority tasks are displayed
4. **Given** multiple tasks exist with different completion statuses, **When** the user filters by "incomplete", **Then** only incomplete tasks are displayed
5. **Given** tasks with due dates exist, **When** the user filters by "has due date", **Then** only tasks with due dates are displayed
6. **Given** multiple tasks exist, **When** the user searches for a keyword in titles/descriptions, **Then** only matching tasks are displayed
7. **Given** multiple tasks exist with different due dates, **When** the user sorts by due date, **Then** tasks appear in chronological order
8. **Given** multiple tasks exist with different priorities, **When** the user sorts by priority, **Then** tasks appear with high priority first, then medium, then low
9. **Given** multiple tasks exist, **When** the user sorts alphabetically by title, **Then** tasks appear in alphabetical order

---

### User Story 3 - Advanced Task Features (Priority: P3)

A user manages tasks with due dates, sets time-based reminders, and creates recurring tasks that automatically generate the next occurrence in memory. The system visually indicates overdue tasks and triggers CLI-based notifications when reminders are due.

**Why this priority**: These features enhance productivity for users with time-sensitive or repetitive tasks, but are not essential for basic task tracking. They represent "nice-to-have" capabilities that build upon the foundation of previous stories.

**Independent Test**: Can be tested by creating a task with a due date in the past, observing overdue status display, and creating a recurring task that generates the next occurrence. Delivers value by proactively alerting users to time-sensitive work.

**Acceptance Scenarios**:

1. **Given** a task is created with a due date in the past, **When** the task is viewed, **Then** it displays as "overdue" with visual indication
2. **Given** a task is created with a future due date, **When** the due date passes during runtime, **Then** the task displays as "overdue"
3. **Given** a task is created with a reminder time, **When** the reminder time is reached during runtime, **Then** the CLI displays a notification message for that task
4. **Given** a task is created with a "daily" recurrence rule, **When** the task is marked complete, **Then** a new task with the same attributes is automatically created for the next day
5. **Given** a task is created with a "weekly" recurrence rule, **When** the task is marked complete, **Then** a new task with the same attributes is automatically created for the next week
6. **Given** a task is created with a custom recurrence interval (e.g., every 3 days), **When** the task is marked complete, **Then** a new task is automatically created for the next interval
7. **Given** a recurring task is marked complete, **When** the next occurrence is generated, **Then** the ID remains unique and attributes (except recurrence generation) are preserved

---

### Edge Cases

- What happens when the user attempts to create a task with an empty title?
- What happens when the user provides an invalid priority value?
- What happens when the user provides an invalid date format for due dates?
- What happens when the user filters by criteria that matches no tasks?
- What happens when the user sorts tasks when no sorting key is applicable (e.g., sorting by due date when none have due dates)?
- What happens when a recurring task with no due date is marked complete?
- What happens when the user searches for a string with special characters?
- What happens when tags contain spaces or special characters?
- What happens when the system has zero tasks and user attempts to view or filter?

## Requirements

### Functional Requirements

#### Core Essentials

- **FR-001**: System MUST allow users to create a new task with a required title and optional description
- **FR-002**: System MUST assign a unique task ID to each created task
- **FR-003**: System MUST allow users to delete a task by providing its ID
- **FR-004**: System MUST allow users to update any existing task's title, description, priority, tags, due date, reminder time, or recurrence rule
- **FR-005**: System MUST display all tasks in a human-readable CLI format
- **FR-006**: System MUST allow users to toggle a task's completion status between complete and incomplete

#### Organization & Usability

- **FR-007**: System MUST allow users to assign a priority level (high, medium, or low) to any task
- **FR-008**: System MUST allow users to assign one or more tags/categories to any task
- **FR-009**: System MUST allow users to search tasks by keyword matching against task titles or descriptions
- **FR-010**: System MUST allow users to filter tasks by completion status (complete, incomplete, or all)
- **FR-011**: System MUST allow users to filter tasks by priority level (high, medium, low, or all)
- **FR-012**: System MUST allow users to filter tasks by presence of due date (has due date, no due date, or all)
- **FR-013**: System MUST allow users to sort tasks by due date (ascending or descending)
- **FR-014**: System MUST allow users to sort tasks by priority (high to low or low to high)
- **FR-015**: System MUST allow users to sort tasks alphabetically by title (ascending or descending)

#### Advanced Features

- **FR-016**: System MUST allow users to assign a due date to any task
- **FR-017**: System MUST visually indicate tasks with due dates in the past as "overdue"
- **FR-018**: System MUST allow users to assign a reminder time to any task
- **FR-019**: System MUST display a CLI notification when a task's reminder time is reached during runtime
- **FR-020**: System MUST support creating recurring tasks with a defined recurrence rule (daily, weekly, or custom interval)
- **FR-021**: System MUST automatically generate the next occurrence of a recurring task in memory when the current task is marked complete
- **FR-022**: System MUST preserve task attributes (except recurrence metadata) when generating recurring task occurrences

#### Error Handling

- **FR-023**: System MUST display clear, human-readable error messages when users provide invalid task IDs
- **FR-024**: System MUST display clear, human-readable error messages when users provide invalid priority values
- **FR-025**: System MUST display clear, human-readable error messages when users provide invalid date formats
- **FR-026**: System MUST handle gracefully when search or filter operations match zero tasks, displaying an appropriate message

#### CLI Behavior

- **FR-027**: System MUST run entirely in the terminal with no graphical interface
- **FR-028**: System MUST support either menu-driven or command-driven user interactions
- **FR-029**: System MUST display output in a consistent, human-readable format across all operations
- **FR-030**: System MUST handle all error conditions gracefully without crashing

### Key Entities

- **Todo Task**: Represents a single task item with the following attributes:
  - Unique identifier (required, auto-generated)
  - Title (required, text)
  - Description (optional, text)
  - Completion status (required, complete/incomplete)
  - Priority (required, high/medium/low)
  - Tags (one or more, text labels)
  - Due date (optional, date/time)
  - Reminder time (optional, date/time)
  - Recurrence rule (optional, defines generation pattern for next occurrence)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can complete the full add-view-update-delete-complete task cycle in under 60 seconds per task
- **SC-002**: Users can find any specific task in a list of 100 tasks in under 10 seconds using search, filter, or sort
- **SC-003**: 100% of task operations complete successfully without system crashes
- **SC-004**: All overdue tasks are correctly identified and visually distinguished in the task list
- **SC-005**: Recurring tasks automatically generate the next occurrence in memory within 1 second of marking the current task complete
- **SC-006**: Time-based reminder notifications display within 5 seconds of the reminder time being reached

### Quality Outcomes

- **SC-007**: All error messages clearly indicate what went wrong and how to fix it
- **SC-008**: The CLI interface is intuitive enough that a new user can successfully complete their first task within 3 minutes of starting the application
- **SC-009**: Task displays are consistently formatted across all views (list view, filtered views, search results)

## Assumptions

- The application runs on a single system with no need for synchronization across devices
- Dates and times use the system's local timezone
- Recurrence intervals are measured in days
- Tag values are case-sensitive unless the user specifies otherwise
- Task IDs are numeric and increment sequentially starting from 1
- The application remains running during the user session (reminders only trigger during runtime)
- When multiple sort criteria are applicable, the primary sort determines the final order
- A task with both a due date and reminder time must have the reminder time before or at the due date to be logical

## Traceability

Every future Plan, Task, and Implementation:

- MUST reference this specification (001-in-memory-todo-cli/spec.md)
- MUST remain compliant with the project constitution
- MUST NOT introduce features explicitly marked as out-of-scope
- MUST preserve the ability to extend to future phases (web UI, persistence, authentication, etc.)
