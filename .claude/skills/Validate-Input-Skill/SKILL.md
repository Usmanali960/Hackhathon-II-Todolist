Overview

This skill provides validation for task inputs to ensure correct, error-free operations in a ToDo List app.

Purpose

This skill allows Claude to:

Validate task titles, descriptions, and due dates

Prevent duplicates

Return structured JSON indicating success or failure

Quick Start

When a task is being added or updated:

Receive input data (title, description, due date)

Check each field for correctness

Return JSON with validation result

Core Capabilities
Input Validation

Ensure title is not empty

Check for duplicate task titles

Validate due date format

Confirm optional description meets requirements

Response Management

Return success/failure JSON

Include detailed error messages

Usage Examples

"Validate task titled 'Buy milk' with due date tomorrow"

"Check if task title is empty or duplicate"

"Validate due date format '2025-12-31'"