# Data Model: Todo Task Entity

**Feature**: 001-in-memory-todo-cli | **Spec Reference**: spec.md (Key Entities section)
**Purpose**: Define the core domain entity with all attributes, validation rules, and lifecycle management.

---

## Entity: Task

The `Task` entity represents a single todo item with all attributes defined in the specification.

### Attributes

| Attribute | Type | Required | Validation | Default |
|-----------|------|----------|------------|---------|
| id | int | Yes | Auto-incrementing, unique, positive integer | Auto-generated |
| title | str | Yes | Non-empty, max 200 characters | None |
| description | str | No | Max 1000 characters | None |
| status | Status | Yes | Must be `Status.INCOMPLETE` or `Status.COMPLETE` | `Status.INCOMPLETE` |
| priority | Priority | Yes | Must be `Priority.HIGH`, `Priority.MEDIUM`, or `Priority.LOW` | `Priority.MEDIUM` |
| tags | Set[str] | Yes | Non-empty set, each tag 1-50 chars, trimmed | `set()` |
| due_date | datetime | No | Must be after creation time | None |
| reminder_time | datetime | No | Must be before or at due_date | None |
| recurrence_rule | RecurrenceRule | No | Must have valid type and interval if custom | None |
| created_at | datetime | Yes | Auto-generated, immutable | Now |
| updated_at | datetime | Yes | Auto-updated on changes | Now |
| reminder_notified | bool | Yes | True if reminder displayed | False |

### Enums

#### Status

```python
class Status(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
```

#### Priority

```python
class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

### Data Classes

#### RecurrenceRule

```python
@dataclass
class RecurrenceRule:
    type: RecurrenceType
    interval_days: int = 1  # Only used for CUSTOM type

class RecurrenceType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"  # Requires interval_days
```

---

## Validation Rules

### Title Validation

- **Required**: Title must not be empty after stripping whitespace
- **Length**: Maximum 200 characters
- **Error Message**: "Title is required. Please provide a task title."

### Description Validation

- **Optional**: May be None or empty string
- **Length**: Maximum 1000 characters if provided
- **Error Message**: "Description exceeds maximum length of 1000 characters."

### Priority Validation

- **Required**: Must be valid Priority enum value
- **Valid Values**: "high", "medium", "low" (case-insensitive)
- **Error Message**: "Invalid priority '{value}'. Allowed values: high, medium, low."

### Tags Validation

- **Required**: Must be a set (can be empty)
- **Tag Length**: Each tag 1-50 characters after trimming
- **Tag Format**: Tags are trimmed of whitespace
- **Duplicate Tags**: Duplicates are removed (set semantics)
- **Error Message**: "Tag '{tag}' exceeds maximum length of 50 characters."

### Due Date Validation

- **Optional**: May be None
- **Timezone**: Uses system local timezone
- **Constraint**: Must be after task creation time
- **Error Message**: "Due date must be in the future."

### Reminder Time Validation

- **Optional**: May be None
- **Timezone**: Uses system local timezone
- **Constraint**: Must be before or at due_date (if due_date exists)
- **Error Message**: "Reminder time must be before or at the due date."

### Recurrence Rule Validation

- **Optional**: May be None
- **Type Validation**: Must be valid RecurrenceType enum
- **Custom Interval**: If type is CUSTOM, interval_days must be positive integer
- **Error Message**: "Custom recurrence requires a positive interval in days."

---

## Lifecycle Management

### Creation

1. **ID Generation**: Auto-incrementing integer starting at 1
2. **Timestamps**: `created_at` and `updated_at` set to current time
3. **Default Values**:
   - status: `Status.INCOMPLETE`
   - priority: `Priority.MEDIUM`
   - tags: empty set
   - reminder_notified: False
4. **Validation**: All validation rules applied before creation

### Update

1. **Immutable Fields**: `id` and `created_at` cannot be modified
2. **Timestamp Update**: `updated_at` automatically set to current time
3. **Validation**: All validation rules applied to modified fields
4. **Tag Updates**: Tags are replaced (merged updates not supported)
5. **Priority Updates**: Can change priority at any time

### Deletion

1. **Soft Delete Not Supported**: Task is permanently removed from in-memory storage
2. **ID Reuse**: IDs are not reused after deletion
3. **Cascade**: Recurring task generation does not cascade on deletion

---

## Methods

### is_overdue() -> bool

Returns `True` if:
- Task has a `due_date`
- `due_date` is before current time
- Task status is `INCOMPLETE`

### should_remind() -> bool

Returns `True` if:
- Task has a `reminder_time`
- `reminder_time` is before or at current time
- `reminder_notified` is `False`

### has_recurrence() -> bool

Returns `True` if:
- Task has a `recurrence_rule`
- `recurrence_rule` is not None

### can_complete() -> bool

Returns `True` if:
- Task status is `INCOMPLETE`

---

## Example Instances

### Minimal Task

```python
Task(
    id=1,
    title="Buy groceries",
    description=None,
    status=Status.INCOMPLETE,
    priority=Priority.MEDIUM,
    tags=set(),
    due_date=None,
    reminder_time=None,
    recurrence_rule=None,
    created_at=datetime(2025, 12, 31, 10, 0, 0),
    updated_at=datetime(2025, 12, 31, 10, 0, 0),
    reminder_notified=False
)
```

### Task with All Features

```python
Task(
    id=2,
    title="Complete project documentation",
    description="Finish all markdown documentation files",
    status=Status.INCOMPLETE,
    priority=Priority.HIGH,
    tags={"work", "documentation"},
    due_date=datetime(2026, 1, 15, 17, 0, 0),
    reminder_time=datetime(2026, 1, 15, 9, 0, 0),
    recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
    created_at=datetime(2025, 12, 31, 10, 0, 0),
    updated_at=datetime(2025, 12, 31, 10, 0, 0),
    reminder_notified=False
)
```

---

## Future Extensibility (Phase II+)

This data model is designed to support future phases:

1. **Persistence Layer**: All attributes can be serialized to database schema
2. **User Association**: Add `user_id` field for multi-user support (Phase II)
3. **Attachments**: Add `attachments` list for file references (Phase II)
4. **Subtasks**: Add `parent_id` field for task hierarchies (Phase II)
5. **AI Context**: Add `ai_generated_notes` field for AI insights (Phase III)

The modular design allows extending without breaking existing functionality.
