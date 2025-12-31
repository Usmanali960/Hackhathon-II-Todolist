"""Fix string formatting issues in menu.py."""

with open('src/cli/menu.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all the problematic format_filter_result calls - they have extra closing braces
# The pattern is: format_filter_result(tasks, f'..."')}") -> format_filter_result(tasks, f'..."')"

fixes = [
    # Line 195 - keyword search
    (r"print\(f\"\n\{self\._formatter\.format_filter_result\(tasks, f'keyword \\\"\\\{keyword\\\"\\'\)\\}\"\)",
     'print(f"\\n{self._formatter.format_filter_result(tasks, f\'keyword \\"{keyword}\\'\\")'),

    # Line 245 - status filter
    (r"print\(f\"\n\{self\._formatter\.format_filter_result\(tasks, f'status \\\"\\\{status\\\"\\'\)\\}\"\)",
     'print(f"\\n{self._formatter.format_filter_result(tasks, f\\'status \\"{status}\\'\\")'),

    # Line 277 - priority filter
    (r"print\(f\"\n\{self\._formatter\.format_filter_result\(tasks, f'priority \\\"\\\{priority\\\"\\'\)\\}\"\)",
     'print(f"\\n{self._formatter.format_filter_result(tasks, f\\'priority \\"{priority}\\'\\")'),

    # Line 306 - due date filter
    (r"print\(f\"\n\{self\._formatter\.format_filter_result\(tasks, 'has due date' if has_due_date else 'no due date'\)\\}\"\)",
     'print(f"\\n{self._formatter.format_filter_result(tasks, \\'has due date\\' if has_due_date else \\'no due date\\')\\")'),
]

for pattern, replacement in fixes:
    content = content.replace(pattern, replacement)

with open('src/cli/menu.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed menu.py")
