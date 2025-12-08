# Expense Tracker

A simple command-line expense tracker application for managing personal expenses with category-based organisation and spending analysis.

## Features

- **Add Expenses**: Record expenses with amount, category, and description
- **View All Expenses**: Display expenses in a formatted table with timestamps
- **Total Spending**: Calculate and display total spending across all expenses
- **Category Analysis**: View spending breakdown by category with percentages
- **Filter by Category**: View expenses filtered by specific categories
- **Data Persistence**: Automatic saving and loading from JSON file
- **Input Validation**: Ensures valid amounts and prevents empty fields

## Installation

### Prerequisites

- Python 3.7 or higher (uses standard library only)

### Setup

1. Clone or download the project:
```bash
git clone <repository-url>
cd expense-tracker
```

2. Run the application (no additional dependencies required):
```bash
python expense_tracker.py
```

## Usage

### Running the CLI

Start the expense tracker by running:

```bash
python expense_tracker.py
```

You'll see the main menu with six options:

```
Welcome to the Expense Tracker!

Select an option:
1. Add expense
2. View all expenses
3. Calculate total spending
4. View spending by category
5. Filter expenses by category
6. Quit
```

### Example Usage Session

```bash
$ python expense_tracker.py

Welcome to the Expense Tracker!

Select an option:
1. Add expense
2. View all expenses
3. Calculate total spending
4. View spending by category
5. Filter expenses by category
6. Quit

Enter your choice (1-6): 1
Enter amount: £25.50
Enter category: Food
Enter description: Lunch at cafe
Expense added: £25.50 for Food

Enter your choice (1-6): 2
================================================================================
ID   Date                 Category        Amount     Description
================================================================================
1    2024-10-09 16:30:45  Food            £25.50     Lunch at cafe
================================================================================
```

### Programmatic Usage

You can also use the `ExpenseTracker` class in your own Python scripts:

```python
from expense_tracker import ExpenseTracker

# Create tracker instance
tracker = ExpenseTracker("my_expenses.json")

# Add expenses
tracker.add_expense(25.50, "Food", "Lunch at cafe")
tracker.add_expense(60.00, "Transport", "Monthly bus pass")

# View spending by category
tracker.view_spending_by_category()

# Get total spending
total = tracker.calculate_total_spending()
print(f"Total spent: £{total}")
```

## API Reference

### ExpenseTracker Class

Main class for managing expenses with the following methods:

#### `__init__(data_file: str = "expenses.json") -> None`

Initialise the expense tracker.

**Parameters:**
- `data_file` (str): Path to the JSON file for storing expenses

#### `add_expense(amount: float, category: str, description: str) -> None`

Add a new expense to the tracker.

**Parameters:**
- `amount` (float): The expense amount (must be positive)
- `category` (str): The expense category
- `description` (str): Description of the expense

#### `view_all_expenses() -> None`

Display all expenses in a formatted table with ID, date, category, amount, and description.

#### `calculate_total_spending() -> float`

Calculate and display the total amount spent across all expenses.

**Returns:**
- `float`: Total spending amount

#### `view_spending_by_category() -> None`

Display spending breakdown by category with amounts and percentages.

#### `filter_by_category(category: str) -> None`

Display expenses filtered by the specified category.

**Parameters:**
- `category` (str): The category to filter by (case-insensitive)

#### `get_available_categories() -> List[str]`

Get a list of all unique categories from recorded expenses.

**Returns:**
- `List[str]`: Sorted list of unique categories

## File Structure

```
expense-tracker/
├── expense_tracker.py    # Main application file
├── expenses.json        # Data storage (created automatically)
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Data Storage

Expenses are stored in JSON format with the following structure:

```json
[
  {
    "id": 1,
    "amount": 25.50,
    "category": "Food",
    "description": "Lunch at cafe",
    "date": "2024-10-09 16:30:45"
  }
]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## Development

### Code Style

- Follows PEP 8 standards
- Uses type hints for all function parameters and returns
- Comprehensive docstrings for all public methods
- UK English spelling conventions

### Testing

The project includes comprehensive unit tests covering all major components.

#### Running Tests

Run the test suite using Python's unittest module:

```bash
# Run all tests with verbose output
python3 -m unittest test_expense_tracker -v

# Run specific test class
python3 -m unittest test_expense_tracker.TestExpenseTracker -v

# Run specific test method
python3 -m unittest test_expense_tracker.TestExpenseTracker.test_add_expense_valid -v
```

#### Test Coverage

The test suite includes 37 tests covering:

- **Expense class**: Creation, serialisation, and deserialisation
- **InputValidator**: Validation of amounts, text fields, and menu choices
- **JsonFileStorage**: Saving and loading data, error handling
- **ExpenseTracker**: All CRUD operations and business logic
- **TableFormatter**: All display and formatting functions
- **ExpenseTrackerUI**: User interface interactions and input handling

All tests are passing with 100% success rate.

#### Manual Testing

You can also manually test the application:

```bash
# Test adding expenses
python3 expense_tracker.py

# Test with different categories and amounts
# Verify data persistence by restarting the application
```

## License

This project is open source. Feel free to use, modify, and distribute.

## Changelog

### v1.0.0
- Initial release with core expense tracking functionality
- CLI interface with 6 main options
- JSON-based data persistence
- Category-based expense organisation
- Spending analysis and filtering capabilities