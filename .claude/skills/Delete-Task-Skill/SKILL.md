Overview

This skill provides capabilities for removing tasks from a ToDo List app safely and efficiently.

Purpose

This skill allows Claude to:

Delete tasks based on task ID or title

Validate task existence before deletion

Return structured JSON confirming deletion

Quick Start

When a user wants to delete a task:

Receive task ID or title

Confirm the task exists

Remove the task from the database

Return success or error status

Core Capabilities
Task Deletion

Delete by task ID or title

Check task exists before deletion

Prevent accidental removal of non-existent tasks

Response Management

Return JSON with success status and message

Include deleted task info if needed

Handle errors gracefully

Usage Examples

"Delete task with ID 123"

"Remove task titled 'Buy groceries'"

"Try deleting task, return error if it doesn’t exist"