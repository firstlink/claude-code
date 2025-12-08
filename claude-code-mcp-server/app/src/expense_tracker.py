"""Main expense tracker class for managing expenses."""

import json
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from .expense import Expense


class ExpenseTracker:
    """Manages a collection of expenses with persistence functionality."""

    def __init__(self, data_file: str = "expenses.json") -> None:
        """Initialize the expense tracker.

        Args:
            data_file: Path to the data file for persistence
        """
        self.data_file = data_file
        self.expenses: List[Expense] = []
        self.load_expenses()

    def add_expense(self, amount: float, category: str, description: str) -> None:
        """Add a new expense to the tracker.

        Args:
            amount: The expense amount
            category: The expense category
            description: The expense description
        """
        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self.save_expenses()

    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses.

        Returns:
            List of all expenses
        """
        return self.expenses.copy()

    def get_total_spending(self) -> float:
        """Calculate total spending across all expenses.

        Returns:
            Total amount spent
        """
        return sum(expense.amount for expense in self.expenses)

    def get_spending_by_category(self) -> Dict[str, float]:
        """Get spending totals grouped by category.

        Returns:
            Dictionary mapping categories to total spending
        """
        category_totals: Dict[str, float] = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        return category_totals

    def filter_by_category(self, category: str) -> List[Expense]:
        """Filter expenses by category.

        Args:
            category: Category to filter by

        Returns:
            List of expenses in the specified category
        """
        return [expense for expense in self.expenses if expense.category.lower() == category.lower()]

    def get_expenses_last_30_days(self) -> List[Expense]:
        """Get expenses from the last 30 days.

        Returns:
            List of expenses from the last 30 days
        """
        thirty_days_ago = datetime.now() - timedelta(days=30)
        return [expense for expense in self.expenses if expense.date >= thirty_days_ago]

    def get_categories(self) -> List[str]:
        """Get all unique categories.

        Returns:
            List of unique category names
        """
        categories = set(expense.category for expense in self.expenses)
        return sorted(list(categories))

    def save_expenses(self) -> None:
        """Save expenses to the data file."""
        try:
            data = [expense.to_dict() for expense in self.expenses]
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        except IOError as e:
            print(f"Error saving expenses: {e}")

    def load_expenses(self) -> None:
        """Load expenses from the data file."""
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.expenses = [Expense.from_dict(item) for item in data]
        except (IOError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading expenses: {e}")
            self.expenses = []