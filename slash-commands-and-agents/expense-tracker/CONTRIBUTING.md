# Contributing to Expense Tracker

Thank you for your interest in contributing to the Expense Tracker project! This guide will help you get started with development and contributions.

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Getting Started

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   # No additional dependencies required - uses Python standard library only
   python3 expense_tracker.py  # Test that it runs
   ```

## Code Style Guidelines

### Python Conventions

- **Follow PEP 8** strictly
- **Use UK English spelling** (colour, optimisation, etc.)
- **Type hints** for all function parameters and returns
- **Descriptive variable names** over abbreviations
- **Snake_case** for variables and functions
- **PascalCase** for classes
- **f-strings** for string formatting
- **Double quotes** for strings
- **Comprehensive docstrings** for all public methods

### Code Formatting

- **88-character line limit** (Black formatter compatible)
- **Import order**: standard library → third-party → local modules
- **Consistent indentation** using 4 spaces

### Example Code Style

```python
from typing import List, Dict, Any
from dataclasses import dataclass

class ExpenseAnalyser:
    """Analyses expense data and provides insights."""

    def __init__(self, expenses: List[Expense]) -> None:
        """
        Initialise the analyser with expense data.

        Args:
            expenses: List of expense objects to analyse
        """
        self.expenses = expenses

    def calculate_monthly_average(self, category: str) -> float:
        """
        Calculate monthly average spending for a category.

        Args:
            category: The expense category to analyse

        Returns:
            Monthly average spending amount
        """
        category_expenses = [
            expense for expense in self.expenses
            if expense.category.lower() == category.lower()
        ]
        total_amount = sum(expense.amount for expense in category_expenses)
        return total_amount / 12  # Assuming yearly data
```

## Architecture Overview

### Core Components

1. **Data Model** (`Expense` dataclass)
   - Immutable expense representation
   - Factory methods for creation
   - Serialisation support

2. **Storage Layer** (`DataStorage` abstract base class)
   - Plugin architecture for different storage backends
   - Currently implements JSON file storage
   - Easy to extend for databases, APIs, etc.

3. **Business Logic** (`ExpenseTracker`)
   - Core expense management operations
   - Validation and data integrity
   - Category management and filtering

4. **Presentation Layer** (`ExpenseTrackerUI`, `TableFormatter`)
   - User interface and formatting
   - Input handling and validation
   - Display logic separation

### Design Patterns Used

- **Strategy Pattern**: `DataStorage` interface allows pluggable storage backends
- **Factory Pattern**: `Expense.create_new()` for object creation
- **Single Responsibility**: Each class has a focused purpose
- **Dependency Injection**: `ExpenseTracker` accepts storage implementation

## Making Changes

### Adding New Features

1. **Plan the feature**
   - Consider impact on existing functionality
   - Design API if adding new public methods
   - Consider storage implications

2. **Implement incrementally**
   ```bash
   # Example: Adding expense categories with budgets

   # 1. Update data model
   @dataclass
   class ExpenseBudget:
       category: str
       monthly_limit: float

   # 2. Update storage
   # Add budget loading/saving to JsonFileStorage

   # 3. Update business logic
   # Add budget tracking to ExpenseTracker

   # 4. Update UI
   # Add budget-related menu options
   ```

3. **Test thoroughly**
   - Test new functionality manually
   - Test edge cases and error conditions
   - Verify backward compatibility

### Adding New Storage Backends

```python
class DatabaseStorage(DataStorage):
    """Example database storage implementation."""

    def __init__(self, connection_string: str) -> None:
        """Initialise with database connection."""
        self.connection_string = connection_string

    def save_expenses(self, expenses: List[Expense]) -> None:
        """Save expenses to database."""
        # Implementation here
        pass

    def load_expenses(self) -> List[Expense]:
        """Load expenses from database."""
        # Implementation here
        return []
```

### Extending the UI

```python
class WebExpenseTrackerUI(ExpenseTrackerUI):
    """Web-based UI implementation."""

    def __init__(self, tracker: ExpenseTracker, port: int = 8000) -> None:
        """Initialise web UI."""
        super().__init__(tracker)
        self.port = port

    def run(self) -> None:
        """Start web server."""
        # Web framework implementation
        pass
```

## Testing Guidelines

### Manual Testing Checklist

When making changes, test the following scenarios:

#### Core Functionality
- [ ] Add expenses with various amounts, categories, descriptions
- [ ] View all expenses in formatted table
- [ ] Calculate total spending
- [ ] View spending by category breakdown
- [ ] Filter expenses by category
- [ ] Quit application gracefully

#### Edge Cases
- [ ] Add expense with £0.01 amount
- [ ] Add expense with very large amount (£999,999.99)
- [ ] Add expense with long description (100 characters)
- [ ] Add expense with special characters in category/description
- [ ] View expenses when none exist
- [ ] Filter by non-existent category
- [ ] Invalid menu choices (0, 7, letters, symbols)

#### Data Persistence
- [ ] Restart application and verify expenses persist
- [ ] Manually corrupt JSON file and verify graceful handling
- [ ] Delete JSON file and verify new file creation

#### Input Validation
- [ ] Enter negative amounts
- [ ] Enter non-numeric amounts
- [ ] Enter empty category/description
- [ ] Enter whitespace-only category/description

### Integration Testing

Test different components working together:

```bash
# Test with different storage implementations
python3 -c "
from expense_tracker import ExpenseTracker, JsonFileStorage
storage = JsonFileStorage('test_expenses.json')
tracker = ExpenseTracker(storage)
tracker.add_expense(10.50, 'Test', 'Integration test')
print(f'Total: £{tracker.calculate_total_spending():.2f}')
"
```

## Submission Guidelines

### Pull Request Process

1. **Ensure code quality**
   - Follow code style guidelines
   - Add appropriate docstrings
   - Test thoroughly

2. **Create descriptive PR**
   ```markdown
   ## Summary
   Brief description of what this PR does

   ## Changes Made
   - List specific changes
   - Include any breaking changes

   ## Testing Done
   - Manual testing scenarios covered
   - Edge cases tested

   ## Screenshots (if UI changes)
   Include before/after screenshots for UI changes
   ```

3. **Use conventional commit messages**
   ```bash
   feat: add expense budgeting functionality
   fix: handle empty JSON file gracefully
   docs: update API documentation for new methods
   refactor: extract validation logic to separate class
   ```

### Branch Naming Convention

- `feature/ticket-description` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation only
- `refactor/code-improvement` - Code refactoring

### Commit Message Format

```
type(scope): brief description

Longer description if needed, explaining:
- What changed
- Why it changed
- Any breaking changes or migration notes

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Code Review Guidelines

### For Contributors

- **Keep PRs focused** - One feature/fix per PR
- **Write clear descriptions** - Explain what and why
- **Respond to feedback** - Address reviewer comments promptly
- **Test your changes** - Ensure functionality works as expected

### For Reviewers

- **Check code style** - Ensure consistency with guidelines
- **Verify functionality** - Test the changes locally
- **Consider edge cases** - Think about error conditions
- **Suggest improvements** - Help make the code better

## Development Workflow

### Typical Development Cycle

1. **Identify improvement/feature needed**
2. **Create issue** (if significant change)
3. **Create feature branch**
4. **Implement changes incrementally**
5. **Test thoroughly**
6. **Update documentation** (if needed)
7. **Submit pull request**
8. **Address review feedback**
9. **Merge when approved**

### Release Process

1. **Version bumping** in `__version__` variable
2. **Update CHANGELOG.md** with new features/fixes
3. **Tag release** with semantic versioning
4. **Update README** if needed

## Getting Help

### Questions and Discussion

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - General questions and ideas
- **Code Comments** - Inline documentation and explanations

### Debugging Common Issues

#### JSON File Corruption
```python
import json
try:
    with open('expenses.json', 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON error at line {e.lineno}, column {e.colno}")
    # Manual fix or restore from backup
```

#### Import Errors
```bash
# Ensure you're in the correct directory
ls -la  # Should see expense_tracker.py

# Check Python version
python3 --version  # Should be 3.7+
```

Thank you for contributing to Expense Tracker! 🎯