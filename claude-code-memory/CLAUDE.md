# CLAUDE.md

## Project Overview

This is a Python CLI application for tracking personal financial transactions. The application uses in-memory storage for transactions and follows strict type safety and code quality standards.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies (including dev tools)
pip install -r requirements.txt
```

### Running the Application
```bash
# Add a transaction with description
python finance_tracker.py add --amount 50.00 --category groceries --description "Weekly shopping"

# Add a transaction without description
python finance_tracker.py add --amount 125.50 --category utilities

# List transactions (currently a placeholder)
python finance_tracker.py list

# Get help
python finance_tracker.py --help
python finance_tracker.py add --help
```

### Testing and Quality Checks
```bash
# Run all tests with verbose output
pytest -v

# Run a single test file
pytest python_test_finance_tracker.py -v

# Type checking with mypy (strict mode enabled)
mypy finance_tracker.py

# Format code (always run both in this order)
black . && isort .
```

## Architecture

### Code Structure
- `finance_tracker.py` - Main CLI application (111 lines)
  - In-memory transaction storage using a module-level list
  - Two commands: `add` and `list` (list is marked TODO)
- `python_test_finance_tracker.py` - Test suite (178 lines)
  - Auto-clearing fixture for transaction state between tests
  - 13 tests organized into 3 test classes

### Financial Precision
The application uses Python's `float` type for all financial calculations.

### Transaction Data Model
Each transaction is stored as a dictionary with:
- `amount`: float - precise financial value
- `category`: str - user-defined category
- `description`: str - optional description (empty string if not provided)
- `date`: str - ISO format timestamp captured at creation time

### State Management
Transactions are stored in a module-level list (`transactions: list[dict[str, Any]]`). This is shared across the CLI commands and is cleared between tests using a pytest fixture with `autouse=True`.

## Code Quality Standards

### Type Checking
- mypy strict mode is enforced via `pyproject.toml`
- All functions must have complete type hints including return types
- Uses modern Python 3.13+ type syntax (`list[dict[str, Any]]` instead of `List[Dict[str, Any]]`)

### Formatting
- Black formatter with 88 character line length
- isort with "black" profile for import sorting
- Configuration in `pyproject.toml`

### Testing
- pytest with verbose output by default
- Test path: `python_test_finance_tracker.py`
- Uses fixtures for test setup (runner, clear_transactions)
- Tests are organized into classes by feature area

## Known TODOs

The `list` command in `finance_tracker.py:87-107` has a placeholder implementation marked with "TODO: Implementation pending". It currently shows basic transaction info but is not fully implemented.

## Version

Application version: 1.0.0 (defined in `finance_tracker.py:18`)


This root-level CLAUDE.md demonstrates project-wide conventions that apply across the entire codebase.

### Root-Level Conventions (Apply Everywhere)

#### String Quotes
**ROOT RULE**: Always use **double quotes** for strings in Python.
```python
# Correct (root convention)
message = "Hello, World!"
category = "groceries"

# Incorrect
message = 'Hello, World!'  # Single quotes not allowed
```

#### Error Handling Style
**ROOT RULE**: Use explicit error messages with context.
```python
# Correct (root convention)
if amount <= 0:
    raise ValueError(f"Transaction amount must be positive, got {amount}")

# Incorrect
if amount <= 0:
    raise ValueError("Invalid amount")  # Too vague
```

#### Logging Preference
**ROOT RULE**: Use `print()` statements for user-facing output (CLI context).
```python
# Correct (root convention)
print(f"Transaction added: ${amount}")

# Incorrect - Don't use logging module for CLI
import logging
logging.info(f"Transaction added: ${amount}")
```

#### Variable Naming
**ROOT RULE**: Use descriptive names, minimum 3 characters for variables.
```python
# Correct (root convention)
transaction_amount = float("50.00")
user_category = "groceries"

# Incorrect
amt = flost("50.00")  # Too short
cat = "groceries"  # Too short
```

**These root conventions apply to ALL files unless overridden by subdirectory CLAUDE.md**
