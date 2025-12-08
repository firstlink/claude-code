# Expense Tracker API Documentation

This document provides comprehensive API documentation for the Expense Tracker application classes and methods.

## Core Classes

### Expense

A dataclass representing a single expense entry.

#### Attributes

- `expense_id` (str): Unique identifier for the expense
- `amount` (float): The expense amount in pounds
- `category` (str): The expense category
- `description` (str): Description of the expense
- `date` (str): Timestamp when the expense was created

#### Methods

##### `create_new(amount: float, category: str, description: str) -> Expense`

Create a new expense with generated ID and current timestamp.

**Parameters:**
- `amount` (float): The expense amount (must be positive)
- `category` (str): The expense category
- `description` (str): Description of the expense

**Returns:**
- `Expense`: New expense instance with auto-generated ID and timestamp

**Example:**
```python
expense = Expense.create_new(25.50, "Food", "Lunch at cafe")
```

##### `to_dict() -> Dict[str, Any]`

Convert expense to dictionary for JSON serialisation.

**Returns:**
- `Dict[str, Any]`: Dictionary representation suitable for JSON storage

##### `from_dict(data: Dict[str, Any]) -> Expense`

Create expense from dictionary.

**Parameters:**
- `data` (Dict[str, Any]): Dictionary containing expense data

**Returns:**
- `Expense`: New expense instance created from dictionary

---

### InputValidator

Static utility class for validating user input.

#### Methods

##### `validate_amount(amount: float) -> bool`

Validate expense amount is positive.

**Parameters:**
- `amount` (float): Amount to validate

**Returns:**
- `bool`: True if amount is positive

##### `validate_text_field(text: str) -> bool`

Validate text field is not empty and has reasonable length.

**Parameters:**
- `text` (str): Text to validate

**Returns:**
- `bool`: True if text is valid (not empty, stripped, and ≤100 characters)

##### `validate_choice(choice: int, min_val: int, max_val: int) -> bool`

Validate menu choice is within range.

**Parameters:**
- `choice` (int): User's choice
- `min_val` (int): Minimum valid value
- `max_val` (int): Maximum valid value

**Returns:**
- `bool`: True if choice is within valid range

---

### TableFormatter

Static utility class for formatting and displaying expense data in tables.

#### Methods

##### `print_separator(width: int, char: str = "=") -> None`

Print a separator line.

**Parameters:**
- `width` (int): Width of the separator line
- `char` (str, optional): Character to use for separator. Defaults to "="

##### `print_expenses_table(expenses: List[Expense]) -> None`

Print expenses in a formatted table.

**Parameters:**
- `expenses` (List[Expense]): List of expenses to display

**Output Format:**
```
================================================================================
ID       Date                 Category        Amount     Description
================================================================================
12345678 2024-10-09 16:30:45  Food            £25.50     Lunch at cafe
================================================================================
```

##### `print_category_breakdown(category_totals: Dict[str, float]) -> None`

Print spending breakdown by category.

**Parameters:**
- `category_totals` (Dict[str, float]): Dictionary mapping categories to totals

##### `print_category_expenses(expenses: List[Expense], category: str) -> None`

Print expenses for a specific category.

**Parameters:**
- `expenses` (List[Expense]): List of expenses to display
- `category` (str): Category name for the header

---

### DataStorage (Abstract Base Class)

Abstract base class defining the interface for data storage implementations.

#### Abstract Methods

##### `save_expenses(expenses: List[Expense]) -> None`

Save expenses to storage. Must be implemented by subclasses.

##### `load_expenses() -> List[Expense]`

Load expenses from storage. Must be implemented by subclasses.

---

### JsonFileStorage

JSON file storage implementation of DataStorage.

#### Constructor

##### `__init__(file_path: str = "expenses.json") -> None`

Initialise with file path.

**Parameters:**
- `file_path` (str, optional): Path to JSON file. Defaults to "expenses.json"

#### Methods

##### `save_expenses(expenses: List[Expense]) -> None`

Save expenses to JSON file.

**Parameters:**
- `expenses` (List[Expense]): List of expenses to save

**Raises:**
- Prints error message if IOError occurs during saving

##### `load_expenses() -> List[Expense]`

Load expenses from JSON file.

**Returns:**
- `List[Expense]`: List of loaded expenses, empty list if file doesn't exist or error occurs

**Error Handling:**
- Returns empty list if file doesn't exist
- Prints error message and returns empty list for IOError, JSONDecodeError, or KeyError

---

### ExpenseTracker

Main expense tracker class managing expenses and operations.

#### Constructor

##### `__init__(storage: DataStorage) -> None`

Initialise the expense tracker.

**Parameters:**
- `storage` (DataStorage): Data storage implementation

#### Methods

##### `add_expense(amount: float, category: str, description: str) -> bool`

Add a new expense to the tracker.

**Parameters:**
- `amount` (float): The expense amount
- `category` (str): The expense category
- `description` (str): Description of the expense

**Returns:**
- `bool`: True if expense was added successfully

**Validation:**
- Amount must be positive
- Category and description must not be empty after stripping

##### `get_all_expenses() -> List[Expense]`

Get all expenses.

**Returns:**
- `List[Expense]`: Copy of all expenses

##### `calculate_total_spending() -> float`

Calculate the total amount spent across all expenses.

**Returns:**
- `float`: Total spending amount

##### `get_spending_by_category() -> Dict[str, float]`

Get spending breakdown by category.

**Returns:**
- `Dict[str, float]`: Dictionary mapping categories to total amounts

##### `filter_by_category(category: str) -> List[Expense]`

Get expenses filtered by category.

**Parameters:**
- `category` (str): The category to filter by (case-insensitive)

**Returns:**
- `List[Expense]`: List of expenses in the specified category

##### `get_available_categories() -> List[str]`

Get a list of all unique categories.

**Returns:**
- `List[str]`: Sorted list of unique categories

##### `save_data() -> None`

Save expenses data using storage implementation.

##### `load_data() -> None`

Load expenses data using storage implementation.

---

### ExpenseTrackerUI

User interface for the expense tracker providing a command-line interface.

#### Constructor

##### `__init__(tracker: ExpenseTracker) -> None`

Initialise with expense tracker instance.

**Parameters:**
- `tracker` (ExpenseTracker): The ExpenseTracker instance to use for data operations

#### Methods

##### `display_menu() -> None`

Display the main menu options.

**Output:**
```
Select an option:
1. Add expense
2. View all expenses
3. Calculate total spending
4. View spending by category
5. Filter expenses by category
6. Quit
```

##### `handle_add_expense() -> None`

Handle adding a new expense with input validation.

**User Input Required:**
- Amount (float)
- Category (string)
- Description (string)

##### `handle_view_all_expenses() -> None`

Handle viewing all expenses in tabular format.

##### `handle_calculate_total() -> None`

Handle calculating and displaying total spending.

##### `handle_view_by_category() -> None`

Handle viewing spending breakdown by category.

##### `handle_filter_by_category() -> None`

Handle filtering expenses by category with interactive category selection.

##### `run() -> None`

Run the main application loop with menu handling and user input processing.

**Features:**
- Continuous menu loop until user quits
- Input validation and error handling
- Graceful handling of Ctrl+C (KeyboardInterrupt)

---

## Constants

- `TABLE_WIDTH_FULL = 80`: Width for full expense tables
- `TABLE_WIDTH_CATEGORY = 50`: Width for category breakdown tables
- `CURRENCY_SYMBOL = "£"`: Currency symbol used throughout the application
- `DATE_FORMAT = "%Y-%m-%d %H:%M:%S"`: Date format for timestamps

## Usage Examples

### Basic Usage

```python
from expense_tracker import ExpenseTracker, JsonFileStorage

# Create storage and tracker
storage = JsonFileStorage("my_expenses.json")
tracker = ExpenseTracker(storage)

# Add expenses
tracker.add_expense(25.50, "Food", "Lunch")
tracker.add_expense(60.00, "Transport", "Monthly pass")

# Get data
total = tracker.calculate_total_spending()
categories = tracker.get_spending_by_category()
food_expenses = tracker.filter_by_category("Food")
```

### Custom Storage Implementation

```python
from expense_tracker import DataStorage, ExpenseTracker
from typing import List

class CustomStorage(DataStorage):
    def __init__(self):
        self.data = []

    def save_expenses(self, expenses: List[Expense]) -> None:
        self.data = expenses.copy()

    def load_expenses(self) -> List[Expense]:
        return self.data.copy()

# Use custom storage
tracker = ExpenseTracker(CustomStorage())
```

### Running the CLI

```python
from expense_tracker import main

# Run the complete CLI application
main()
```