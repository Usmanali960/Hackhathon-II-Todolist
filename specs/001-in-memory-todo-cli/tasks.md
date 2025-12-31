# Tasks: Hackathon II Phase I - In-Memory Todo Application (CLI)

**Input**: Design documents from `/specs/001-in-memory-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/task-operations.md

**Tests**: Tests are included in this task list to ensure quality and stability (per plan Step 7 requirements).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths below follow plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per implementation plan (src/, tests/, src/models/, src/services/, src/cli/, src/utils/)
- [X] T002 Create pyproject.toml with Python 3.13+ configuration and UV package manager
- [X] T003 Create module __init__.py files (src/__init__.py, src/models/__init__.py, src/services/__init__.py, src/cli/__init__.py, src/utils/__init__.py, tests/__init__.py, tests/unit/__init__.py, tests/integration/__init__.py)
- [X] T004 [P] Create README.md with project description and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create enums (Status, Priority, RecurrenceType) in src/models/enums.py
- [X] T006 Create RecurrenceRule dataclass in src/models/recurrence_rule.py
- [X] T007 [P] Create validator utility functions (validate_title, validate_priority, validate_tags) in src/utils/validators.py
- [X] T008 [P] Create datetime parser utility (parse_date, parse_time) in src/utils/datetime_parser.py
- [X] T009 Create Task entity class with all attributes and validation in src/models/task.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Deliver full Basic Level functionality (add, delete, update, view, mark complete)

**Independent Test**: Create a task, view it, mark complete, delete it. This delivers immediate value by allowing users to track simple task lists.

### Tests for User Story 1

- [ ] T010 [P] [US1] Create unit tests for Task model in tests/unit/test_task_model.py (Task creation, validation, ID generation)
- [ ] T011 [P] [US1] Create unit tests for TaskStore in tests/unit/test_task_store.py (add, get, delete, update, list operations)
- [ ] T012 [P] [US1] Create integration test for basic CLI workflow in tests/integration/test_cli_basic.py (full task lifecycle: create -> view -> update -> complete -> delete)

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create TaskStore class with in-memory storage in src/services/task_store.py (add, get, delete, update, list_all, exists, count)
- [ ] T014 [US1] Create TaskOperations service with basic CRUD methods in src/services/task_operations.py (create_task, delete_task, update_task, get_all_tasks, toggle_complete)
- [ ] T015 [P] [US1] Create CLIFormatter class with output methods in src/cli/formatter.py (format_task, format_list, format_error, format_success, format_empty_list)
- [ ] T016 [P] [US1] Create CLI command handlers in src/cli/commands.py (handle_add, handle_delete, handle_update, handle_list, handle_complete)
- [ ] T017 [US1] Create menu-driven CLI interface in src/cli/menu.py (main menu loop, input prompts, sub-menus)
- [ ] T018 [US1] Create main CLI entry point with menu and command-line support in src/cli/main.py (main function, argument parsing, error handling)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Organization (Priority: P2)

**Goal**: Deliver Intermediate Level usability (priorities, tags, search, filter, sort)

**Independent Test**: Create multiple tasks with different priorities and tags, then filter by specific priority and sort by due date. Delivers value by reducing time spent locating relevant tasks.

### Tests for User Story 2

- [ ] T019 [P] [US2] Create unit tests for TaskOperations organization methods in tests/unit/test_task_operations_org.py (search, filter, sort functionality)
- [ ] T020 [P] [US2] Create integration test for organization workflow in tests/integration/test_cli_organization.py (create multiple tasks -> filter -> sort -> search)

### Implementation for User Story 2

- [ ] T021 [P] [US2] Extend TaskOperations with search_tasks method in src/services/task_operations.py (search by keyword in title/description)
- [ ] T022 [P] [US2] Extend TaskOperations with filter methods in src/services/task_operations.py (filter_by_status, filter_by_priority, filter_by_due_date)
- [ ] T023 [P] [US2] Extend TaskOperations with sort methods in src/services/task_operations.py (sort_by_due_date, sort_by_priority, sort_by_title)
- [ ] T024 [US2] Add CLI command handlers for organization features in src/cli/commands.py (handle_search, handle_filter, handle_sort)
- [ ] T025 [US2] Extend menu-driven interface with organization sub-menus in src/cli/menu.py (filter menu, sort menu, search prompt)
- [ ] T026 [US2] Extend CLIFormatter with filter/sort result formatting in src/cli/formatter.py (format_filter_result)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Advanced Task Features (Priority: P3)

**Goal**: Deliver Advanced Level features (due dates, reminders, recurring tasks) without background services

**Independent Test**: Create a task with a due date in the past, observe overdue status display, and create a recurring task that generates next occurrence. Delivers value by proactively alerting users to time-sensitive work.

### Tests for User Story 3

- [ ] T027 [P] [US3] Create unit tests for RecurrenceEngine in tests/unit/test_recurrence_engine.py (daily, weekly, custom recurrence calculation)
- [ ] T028 [P] [US3] Create unit tests for datetime parser in tests/unit/test_datetime_parser.py (date/time parsing and validation)
- [ ] T029 [P] [US3] Create integration test for advanced workflow in tests/integration/test_cli_advanced.py (recurring task with due date and reminder)

### Implementation for User Story 3

- [ ] T030 [P] [US3] Create RecurrenceEngine class in src/services/recurrence_engine.py (calculate_next_occurrence, calculate_next_due_date, calculate_next_reminder_time)
- [ ] T031 [US3] Extend datetime parser with robust date/time parsing in src/utils/datetime_parser.py (support YYYY-MM-DD, MM/DD/YYYY, HH:MM formats)
- [ ] T032 [US3] Extend Task entity with advanced attributes in src/models/task.py (due_date, reminder_time, recurrence_rule, is_overdue, should_remind, has_recurrence methods)
- [ ] T033 [US3] Extend TaskOperations with recurrence integration in src/services/task_operations.py (toggle_complete generates next occurrence, get_overdue_tasks, get_due_reminders, mark_reminder_notified)
- [ ] T034 [P] [US3] Add CLI command handlers for advanced features in src/cli/commands.py (handle_add_with_dates, handle_recurrence)
- [ ] T035 [US3] Implement runtime reminder polling system in src/cli/main.py (check reminders every 5 seconds during idle, display notification)
- [ ] T036 [US3] Extend CLIFormatter with overdue indicator and reminder formatting in src/cli/formatter.py (format_reminder, overdue display in format_task)
- [ ] T037 [US3] Extend menu-driven interface with advanced options in src/cli/menu.py (due date input, reminder input, recurrence rule input)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: CLI Interaction Design

**Purpose**: Polish CLI experience with clear error handling and consistent formatting

- [ ] T038 [P] Extend input validation with edge case handling in src/utils/validators.py (empty title, invalid priority, invalid date format, special characters in tags)
- [ ] T039 [P] Enhance error messages with specific guidance in src/cli/formatter.py (invalid ID suggests available IDs, invalid date suggests valid formats)
- [ ] T040 Implement command-line argument parsing in src/cli/main.py (argparse for add, list, delete, update, complete, search, filter, sort commands with --help)
- [ ] T041 Extend error handling at CLI level in src/cli/main.py (catch all exceptions, never crash, return to menu/prompt)
- [ ] T042 Ensure consistent formatting across all views in src/cli/formatter.py (list view, search results, filtered views use same visual indicators)

---

## Phase 7: Quality & Stability Review

**Purpose**: Validate all features, edge cases, and performance targets

### Unit Test Coverage

- [ ] T043 [P] Create unit tests for validators in tests/unit/test_validators.py (edge cases: empty title, invalid priority, invalid date, tags with spaces)
- [ ] T044 [P] Create unit tests for CLIFormatter in tests/unit/test_formatter.py (format_task, format_list, format_error, format_reminder, format_empty_list)

### Integration Test Coverage

- [ ] T045 [P] Extend integration test for edge cases in tests/integration/test_cli_edge_cases.py (empty list, invalid IDs, filter with zero results, sort with no applicable key)

### Edge Case Validation

- [ ] T046 [P] Validate empty title input rejection with clear error message
- [ ] T047 [P] Validate invalid priority value rejection with allowed values listed
- [ ] T048 [P] Validate invalid date format rejection with valid format suggestions
- [ ] T049 [P] Validate filter with zero results displays appropriate message
- [ ] T050 [P] Validate sort with no applicable key displays appropriate message
- [ ] T051 [P] Validate recurring task without due date generates task correctly
- [ ] T052 [P] Validate search with special characters works correctly
- [ ] T053 [P] Validate tags with spaces trimmed correctly
- [ ] T054 [P] Validate zero tasks list displays appropriate message

### Performance Validation

- [ ] T055 Measure CRUD operation time for 100 tasks (< 1 second)
- [ ] T056 Measure search/filter/sort time for 100 tasks (< 1 second)
- [ ] T057 Measure reminder notification latency (< 5 seconds)

### Extensibility Review

- [ ] T058 Verify domain model can be extended with persistence layer (Phase II)
- [ ] T059 Verify CLI interface can be replaced with web UI (Phase II)
- [ ] T060 Verify TaskOperations can be wrapped as MCP tools (Phase III)
- [ ] T061 Verify code follows modular principles for future refactoring

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **CLI Interaction Design (Phase 6)**: Depends on all user stories being complete
- **Quality & Stability Review (Phase 7)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends US1 TaskOperations and formatter
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Extends US1 TaskOperations and formatter

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/CLI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create unit tests for Task model in tests/unit/test_task_model.py"
Task: "Create unit tests for TaskStore in tests/unit/test_task_store.py"
Task: "Create integration test for basic CLI workflow in tests/integration/test_cli_basic.py"

# Launch all models and services for User Story 1 together:
Task: "Create TaskStore class with in-memory storage in src/services/task_store.py"
Task: "Create TaskOperations service with basic CRUD methods in src/services/task_operations.py"

# Launch all CLI components for User Story 1 together:
Task: "Create CLIFormatter class with output methods in src/cli/formatter.py"
Task: "Create CLI command handlers in src/cli/commands.py"
Task: "Create menu-driven CLI interface in src/cli/menu.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Demo MVP if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo MVP
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
5. Polish CLI interaction → Final validation
6. Quality & stability review → Phase I complete
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently
4. Team completes CLI Interaction Design together
5. Team completes Quality & Stability Review together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

**Total Tasks**: 61
**Tasks Per User Story**:
- Setup: 4 tasks
- Foundational: 5 tasks
- User Story 1: 9 tasks (including tests)
- User Story 2: 8 tasks (including tests)
- User Story 3: 11 tasks (including tests)
- CLI Interaction Design: 5 tasks
- Quality & Stability Review: 19 tasks

**Parallel Opportunities Identified**: 28 tasks marked [P] for parallel execution

**Independent Test Criteria**:
- US1: Create → View → Update → Complete → Delete (full lifecycle)
- US2: Create multiple tasks → Filter by priority → Sort → Search
- US3: Create task with due date → Observe overdue → Create recurring task → Verify next occurrence

**MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1) = 18 tasks
**Full Phase I**: All 61 tasks

---

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, [P] marker where applicable, [Story] label, file paths)
