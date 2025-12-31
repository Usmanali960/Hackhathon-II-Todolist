Overview

This skill provides full capabilities for creating new tasks in a ToDo List application. It ensures tasks are properly validated, stored, and ready for management by other components.

Purpose

This skill allows Claude to:

Add new tasks with a title, description, and optional due date

Validate task input to prevent errors or duplicates

Return structured JSON confirming task creation

Quick Start

When a user wants to add a task:

Collect task information: title, description, due date

Validate the task input

Add the task to the database or storage

Return confirmation with task ID and status

Core Capabilities
Task Creation

Add tasks with mandatory title

Optionally include description and due date

Ensure no duplicate titles exist

Assign unique task ID

Validation

Check that title is not empty

Validate due date format

Confirm input meets all rules

Response Management

Return success or error messages in JSON

Include task ID, title, and status

Handle validation errors gracefully

Usage Examples

"Add a new task called 'Finish report' with due date tomorrow"

"Create a task 'Buy groceries' with description 'Milk, eggs, bread'"

"Add task but return error if title is empty"