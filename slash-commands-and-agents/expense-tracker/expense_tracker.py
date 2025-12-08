"""
Simple expense tracker application for managing personal expenses.

This module provides a comprehensive expense tracking system with the following features:
- Add, view, and categorise expenses
- Calculate total spending and spending by category
- Persistent storage using JSON files
- Command-line user interface
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from uuid import uuid4


# Constants
TABLE_WIDTH_FULL = 80
TABLE_WIDTH_CATEGORY = 50
CURRENCY_SYMBOL = "£"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class Expense:
    """Represents a single expense entry."""
    expense_id: str
    amount: float
    category: str
    description: str
    date: str

    @classmethod
    def create_new(cls, amount: float, category: str, description: str) -> "Expense":
        """Create a new expense with generated ID and current timestamp."""
        return cls(
            expense_id=str(uuid4()),
            amount=amount,
            category=category,
            description=description,
            date=datetime.now().strftime(DATE_FORMAT)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert expense to dictionary for JSON serialisation."""
        return {
            "id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Create expense from dictionary."""
        return cls(
            expense_id=data["id"],
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data["date"]
        )


class InputValidator:
    """Validates user input for expense data."""

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate expense amount is positive."""
        return amount > 0

    @staticmethod
    def validate_text_field(text: str) -> bool:
        """Validate text field is not empty and has reasonable length."""
        stripped_text = text.strip()
        return bool(stripped_text) and len(stripped_text) <= 100

    @staticmethod
    def validate_choice(choice: int, min_val: int, max_val: int) -> bool:
        """Validate menu choice is within range."""
        return min_val <= choice <= max_val


class TableFormatter:
    """Handles formatting and display of expense data in tables.

    This class provides static methods for formatting various types of expense
    reports and tables with consistent styling.
    """

    @staticmethod
    def print_separator(width: int, char: str = "=") -> None:
        """Print a separator line."""
        print(char * width)

    @staticmethod
    def print_expenses_table(expenses: List[Expense]) -> None:
        """Print expenses in a formatted table."""
        if not expenses:
            print("No expenses recorded.")
            return

        TableFormatter.print_separator(TABLE_WIDTH_FULL)
        print(f"{'ID':<8} {'Date':<20} {'Category':<15} {'Amount':<10} {'Description'}")
        TableFormatter.print_separator(TABLE_WIDTH_FULL)

        for expense in expenses:
            expense_id_short = expense.expense_id[:8]
            print(f"{expense_id_short:<8} {expense.date:<20} {expense.category:<15} "
                  f"{CURRENCY_SYMBOL}{expense.amount:<9.2f} {expense.description}")
        TableFormatter.print_separator(TABLE_WIDTH_FULL)

    @staticmethod
    def print_category_breakdown(category_totals: Dict[str, float]) -> None:
        """Print spending breakdown by category."""
        TableFormatter.print_separator(TABLE_WIDTH_CATEGORY)
        print("Spending by Category")
        TableFormatter.print_separator(TABLE_WIDTH_CATEGORY)
        print(f"{'Category':<20} {'Amount':<15} {'Percentage'}")
        print("-" * TABLE_WIDTH_CATEGORY)

        total_spending = sum(category_totals.values())
        for category, amount in sorted(category_totals.items()):
            percentage = (amount / total_spending) * 100 if total_spending > 0 else 0
            print(f"{category:<20} {CURRENCY_SYMBOL}{amount:<14.2f} {percentage:.1f}%")

        print("-" * TABLE_WIDTH_CATEGORY)
        print(f"{'Total':<20} {CURRENCY_SYMBOL}{total_spending:<14.2f} 100.0%")
        TableFormatter.print_separator(TABLE_WIDTH_CATEGORY)

    @staticmethod
    def print_category_expenses(expenses: List[Expense], category: str) -> None:
        """Print expenses for a specific category."""
        if not expenses:
            print(f"No expenses found for category: {category}")
            return

        TableFormatter.print_separator(TABLE_WIDTH_FULL)
        print(f"Expenses for Category: {category}")
        TableFormatter.print_separator(TABLE_WIDTH_FULL)
        print(f"{'ID':<8} {'Date':<20} {'Amount':<10} {'Description'}")
        TableFormatter.print_separator(TABLE_WIDTH_FULL)

        total_for_category = 0
        for expense in expenses:
            expense_id_short = expense.expense_id[:8]
            print(f"{expense_id_short:<8} {expense.date:<20} "
                  f"{CURRENCY_SYMBOL}{expense.amount:<9.2f} {expense.description}")
            total_for_category += expense.amount

        TableFormatter.print_separator(TABLE_WIDTH_FULL)
        print(f"Total for {category}: {CURRENCY_SYMBOL}{total_for_category:.2f}")
        print(f"Number of expenses: {len(expenses)}")


class DataStorage(ABC):
    """Abstract base class for data storage."""

    @abstractmethod
    def save_expenses(self, expenses: List[Expense]) -> None:
        """Save expenses to storage."""
        pass

    @abstractmethod
    def load_expenses(self) -> List[Expense]:
        """Load expenses from storage."""
        pass


class JsonFileStorage(DataStorage):
    """JSON file storage implementation."""

    def __init__(self, file_path: str = "expenses.json") -> None:
        """Initialise with file path."""
        self.file_path = file_path

    def save_expenses(self, expenses: List[Expense]) -> None:
        """Save expenses to JSON file."""
        try:
            expense_dicts = [expense.to_dict() for expense in expenses]
            with open(self.file_path, "w") as file:
                json.dump(expense_dicts, file, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load_expenses(self) -> List[Expense]:
        """Load expenses from JSON file."""
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r") as file:
                expense_dicts = json.load(file)
                return [Expense.from_dict(data) for data in expense_dicts]
        except (IOError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading data: {e}")
            return []


class ExpenseTracker:
    """Main expense tracker class managing expenses and operations."""

    def __init__(self, storage: DataStorage) -> None:
        """
        Initialise the expense tracker.

        Args:
            storage: Data storage implementation
        """
        self.storage = storage
        self.expenses: List[Expense] = []
        self.load_data()

    def add_expense(self, amount: float, category: str, description: str) -> bool:
        """
        Add a new expense to the tracker.

        Args:
            amount: The expense amount
            category: The expense category
            description: Description of the expense

        Returns:
            True if expense was added successfully
        """
        if not InputValidator.validate_amount(amount):
            return False
        if not InputValidator.validate_text_field(category):
            return False
        if not InputValidator.validate_text_field(description):
            return False

        expense = Expense.create_new(amount, category.strip(), description.strip())
        self.expenses.append(expense)
        self.save_data()
        print(f"Expense added: {CURRENCY_SYMBOL}{amount:.2f} for {category}")
        return True

    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses."""
        return self.expenses.copy()

    def calculate_total_spending(self) -> float:
        """
        Calculate the total amount spent across all expenses.

        Returns:
            Total spending amount
        """
        total = sum(expense.amount for expense in self.expenses)
        return total

    def get_spending_by_category(self) -> Dict[str, float]:
        """
        Get spending breakdown by category.

        Returns:
            Dictionary mapping categories to total amounts
        """
        category_totals: Dict[str, float] = {}
        for expense in self.expenses:
            category = expense.category
            category_totals[category] = category_totals.get(category, 0) + expense.amount
        return category_totals

    def filter_by_category(self, category: str) -> List[Expense]:
        """
        Get expenses filtered by category.

        Args:
            category: The category to filter by

        Returns:
            List of expenses in the specified category
        """
        return [expense for expense in self.expenses
                if expense.category.lower() == category.lower()]

    def get_available_categories(self) -> List[str]:
        """
        Get a list of all unique categories.

        Returns:
            List of unique categories
        """
        categories = list(set(expense.category for expense in self.expenses))
        return sorted(categories)

    def save_data(self) -> None:
        """Save expenses data using storage implementation."""
        self.storage.save_expenses(self.expenses)

    def load_data(self) -> None:
        """Load expenses data using storage implementation."""
        self.expenses = self.storage.load_expenses()


class ExpenseTrackerUI:
    """User interface for the expense tracker."""

    def __init__(self, tracker: ExpenseTracker) -> None:
        """
        Initialise with expense tracker instance.

        Args:
            tracker: The ExpenseTracker instance to use for data operations
        """
        self.tracker = tracker
        self.formatter = TableFormatter()

    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\nSelect an option:")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Calculate total spending")
        print("4. View spending by category")
        print("5. Filter expenses by category")
        print("6. Quit")

    def handle_add_expense(self) -> None:
        """Handle adding a new expense with input validation."""
        try:
            amount_str = input(f"Enter amount: {CURRENCY_SYMBOL}")
            amount = float(amount_str)

            if amount <= 0:
                print("Amount must be positive!")
                return

            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()

            if not self.tracker.add_expense(amount, category, description):
                print("Failed to add expense. Please check your input.")

        except ValueError:
            print("Invalid amount! Please enter a valid number.")

    def handle_view_all_expenses(self) -> None:
        """Handle viewing all expenses."""
        expenses = self.tracker.get_all_expenses()
        self.formatter.print_expenses_table(expenses)

    def handle_calculate_total(self) -> None:
        """Handle calculating total spending."""
        total = self.tracker.calculate_total_spending()
        print(f"\nTotal spending: {CURRENCY_SYMBOL}{total:.2f}")

    def handle_view_by_category(self) -> None:
        """Handle viewing spending by category."""
        category_totals = self.tracker.get_spending_by_category()
        if not category_totals:
            print("No expenses recorded.")
            return
        self.formatter.print_category_breakdown(category_totals)

    def handle_filter_by_category(self) -> None:
        """Handle filtering expenses by category."""
        categories = self.tracker.get_available_categories()
        if not categories:
            print("No categories available. Add some expenses first!")
            return

        print("\nAvailable categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")

        try:
            cat_choice = int(input(f"\nSelect category (1-{len(categories)}): "))
            if InputValidator.validate_choice(cat_choice, 1, len(categories)):
                selected_category = categories[cat_choice - 1]
                filtered_expenses = self.tracker.filter_by_category(selected_category)
                self.formatter.print_category_expenses(filtered_expenses, selected_category)
            else:
                print(f"Invalid choice! Please enter a number between 1-{len(categories)}.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to the Expense Tracker!")

        while True:
            self.display_menu()

            try:
                choice = input("\nEnter your choice (1-6): ").strip()

                if choice == "1":
                    self.handle_add_expense()
                elif choice == "2":
                    self.handle_view_all_expenses()
                elif choice == "3":
                    self.handle_calculate_total()
                elif choice == "4":
                    self.handle_view_by_category()
                elif choice == "5":
                    self.handle_filter_by_category()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice! Please enter a number between 1-6.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break


def main() -> None:
    """Main function to run the expense tracker CLI."""
    storage = JsonFileStorage()
    tracker = ExpenseTracker(storage)
    ui = ExpenseTrackerUI(tracker)
    ui.run()


if __name__ == "__main__":
    main()