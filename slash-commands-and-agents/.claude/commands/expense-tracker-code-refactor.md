---
description: Refactor Python code for better quality
argument-hint: [file-path]
allowed-tools: Bash(cat:*), Bash(python:*), Bash(pytest:*)
---

# Refactor Python Code: $ARGUMENTS
Refactor the Python file to improve code quality and readability.

If $ARGUMENTS is empty:
Refactor the entire codebase

## Steps

1. **Read the file:** `cat $ARGUMENTS`
2. **Analyze the code** and identify issues:
   - Long functions (over 50 lines)
   - Duplicate code
   - Complex nested loops
   - Missing docstrings
   - Poor variable names
   - Magic numbers

3. **Create improved version** with:
   - Obeject Oriented approach
   - Clear function names
   - Extracted repeated code
   - Better variable names
   - Type hints
   - Constants for magic numbers

4. **Run tests** to ensure nothing broke: `pytest tests/ -v`

5. **Show before/after comparison**

## Refactoring Checklist

Functions are small (under 50 lines)
Each function does one thing
Good variable and function names
Docstrings added
Type hints included
No duplicate code
Tests still pass