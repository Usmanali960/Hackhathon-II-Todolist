"""Fix string formatting issues in menu.py."""

with open('src/cli/menu.py', 'r') as f:
    lines = f.readlines()

# Fix line 195 (index 194) - remove extra }
if "keyword" in lines[194]:
    lines[194] = lines[194].replace("',)\\}\\\"\\\"", "',')\\\"\\\"\n")

# Fix line 245 (index 244) - remove extra }
if "status" in lines[244]:
    lines[244] = lines[244].replace("',)\\}\\\"\\\"", "',')\\\"\\\"\n")

# Fix line 277 (index 276) - remove extra }
if "priority" in lines[276]:
    lines[276] = lines[276].replace("',)\\}\\\"\\\"", "',')\\\"\\\"\n")

# Fix line 306 (index 305) - remove extra }
if "has due date" in lines[305]:
    lines[305] = lines[305].replace("',)\\}\\\"\\\"", "',')\\\"\\\"\n")

with open('src/cli/menu.py', 'w') as f:
    f.writelines(lines)

print("Fixed")
