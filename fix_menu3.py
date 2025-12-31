"""Fix string formatting issues in menu.py."""

with open('src/cli/menu.py', 'rb') as f:
    content = f.read()

# Replace pattern: format_filter_result(tasks, f'...')}")  ->  format_filter_result(tasks, f'...') ")
# The issue is we have an extra } before the closing quote
# Pattern to fix: ')}")  ->  ')}")

# Find and replace the problematic pattern
# Looking for: format_filter_result(tasks, f'keyword "{keyword}"')}")

content = content.replace(
    b"keyword \"{keyword}\"')}")\\n\"\n",
    b"keyword \"{keyword}\"')}\\n\"\n"
)

content = content.replace(
    b"status \"{status}\"')}")\\n\"\n",
    b"status \"{status}\"')}\\n\"\n"
)

content = content.replace(
    b"priority \"{priority}\"')}")\\n\"\n",
    b"priority \"{priority}\"')}\\n\"\n"
)

content = content.replace(
    b"has due date' if has_due_date else 'no due date')}\"\\n\"\n",
    b"has due date' if has_due_date else 'no due date')\\n\"\n"
)

with open('src/cli/menu.py', 'wb') as f:
    f.write(content)

print('Fixed menu.py with byte-level replacement')
